/*
 * Intel NUC LED Control Driver
 *
 * Copyright (C) 2017 Miles Peterson
 *
 * Portions based on asus-wmi.c:
 * Copyright (C) 2010 Intel Corporation.
 * Copyright (C) 2010-2011 Corentin Chary <corentin.chary@gmail.com>
 *
 * Portions based on acpi_call.c:
 * Copyright (C) 2010: Michal Kottman
 *
 * Based on Intel Article ID 000023426
 * http://www.intel.com/content/www/us/en/support/boards-and-kits/intel-nuc-kits/000023426.html
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/proc_fs.h>
#include <linux/acpi.h>
#include <linux/vmalloc.h>
#include <linux/uaccess.h>

MODULE_AUTHOR("Miles Peterson");
MODULE_DESCRIPTION("Intel NUC LED Control WMI Driver");
MODULE_LICENSE("GPL");
ACPI_MODULE_NAME("NUC_LED");

static unsigned int nuc_led_perms __read_mostly = S_IRUGO | S_IWUSR | S_IWGRP;
static unsigned int nuc_led_uid __read_mostly;
static unsigned int nuc_led_gid __read_mostly;

module_param(nuc_led_perms, uint, S_IRUGO | S_IWUSR | S_IWGRP);
module_param(nuc_led_uid, uint, 0);
module_param(nuc_led_gid, uint, 0);

MODULE_PARM_DESC(nuc_led_perms, "permissions on /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_uid, "default owner of /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_gid, "default owning group of /proc/acpi/nuc_led");

/* Intel NUC WMI GUID */
#define NUCLED_WMI_MGMT_GUID            "8C5DA44C-CDC3-46b3-8619-4E26D34390B7"
MODULE_ALIAS("wmi:" NUCLED_WMI_MGMT_GUID);

/* LED Control Method ID */
#define NUCLED_WMI_METHODID_GETSTATE    0x01
#define NUCLED_WMI_METHODID_SETSTATE    0x02

/* LED Identifiers */
#define NUCLED_WMI_POWER_LED_ID         0x01
#define NUCLED_WMI_RING_LED_ID          0x02

/* Return codes */
#define NUCLED_WMI_RETURN_SUCCESS       0x00
#define NUCLED_WMI_RETURN_NOSUPPORT     0xE1
#define NUCLED_WMI_RETURN_UNDEFINED     0xE2
#define NUCLED_WMI_RETURN_NORESPONSE    0xE3
#define NUCLED_WMI_RETURN_BADPARAM      0xE4
#define NUCLED_WMI_RETURN_UNEXPECTED    0xEF

/* Blink and fade */
#define NUCLED_WMI_BLINK_1HZ            0x01
#define NUCLED_WMI_BLINK_0_25HZ         0x02
#define NUCLED_WMI_FADE_1HZ             0x03
#define NUCLED_WMI_ALWAYS_ON            0x04
#define NUCLED_WMI_BLINK_0_5HZ          0x05
#define NUCLED_WMI_FADE_0_25HZ          0x06
#define NUCLED_WMI_FADE_0_5HZ           0x07

/* Power button colors */
#define NUCLED_WMI_POWER_COLOR_DISABLE  0x00
#define NUCLED_WMI_POWER_COLOR_BLUE     0x01
#define NUCLED_WMI_POWER_COLOR_AMBER    0x02

/* Ring colors */
#define NUCLED_WMI_RING_COLOR_DISABLE   0x00
#define NUCLED_WMI_RING_COLOR_CYAN      0x01
#define NUCLED_WMI_RING_COLOR_PINK      0x02
#define NUCLED_WMI_RING_COLOR_YELLOW    0x03
#define NUCLED_WMI_RING_COLOR_BLUE      0x04
#define NUCLED_WMI_RING_COLOR_RED       0x05
#define NUCLED_WMI_RING_COLOR_GREEN     0x06
#define NUCLED_WMI_RING_COLOR_WHITE     0x07

extern struct proc_dir_entry *acpi_root_dir;

struct led_get_state_args {
        u32 led;
} __packed;

struct led_get_state_return {
        u32 return_code;
        u32 brightness;
        u32 blink_fade;
        u32 color_state;
} __packed;

struct led_set_state_args {
        u8 led;
        u8 brightness;
        u8 blink_fade;
        u8 color_state;
}__packed;

struct led_set_state_return {
        u32 brightness_return;
        u32 blink_fade_return;
        u32 color_return;
} __packed;

#define BUFFER_SIZE 512
static char result_buffer[BUFFER_SIZE];
static char *get_buffer_end(void) {
    return result_buffer + strlen(result_buffer);
}

/* Convert blink/fade value to text */
static const char* const blink_fade_text[] = { "Off", "1Hz Blink", "0.25Hz Blink", "1Hz Fade", "Always On", "0.5Hz Blink", "0.25Hz Fade", "0.5Hz Fade" };

/* Convert color value to text */
static const char* const pwrcolor_text[] =   { "Off", "Blue", "Amber" };
static const char* const ringcolor_text[] =  { "Off", "Cyan", "Pink", "Yellow", "Blue", "Red", "Green", "White" };

/* Get LED state */
static int nuc_led_get_state(u32 led, struct led_get_state_return *state)
{
        struct led_get_state_args args = {
                .led = led
        };
        struct acpi_buffer input;
        struct acpi_buffer output = { ACPI_ALLOCATE_BUFFER, NULL };
        acpi_status status;
        union acpi_object *obj;

        input.length = (acpi_size) sizeof(args);
        input.pointer = &args;

	// Per Intel docs, first instance is used (instance is indexed from 0)
        status = wmi_evaluate_method(NUCLED_WMI_MGMT_GUID, 0, NUCLED_WMI_METHODID_GETSTATE,
                                     &input, &output);

        if (ACPI_FAILURE(status))
	{
		ACPI_EXCEPTION((AE_INFO, status, "wmi_evaluate_method"));
                return -EIO;
	}

        // Always returns a buffer
        obj = (union acpi_object *)output.pointer;
        if (obj && state)
        {
                state->return_code = obj->buffer.pointer[0];
                state->brightness  = obj->buffer.pointer[1];
                state->blink_fade  = obj->buffer.pointer[2];
                state->color_state = obj->buffer.pointer[3];
        }

        kfree(obj);

        return 0;
}

/* Set LED state */
static int nuc_led_set_state(u32 led, u32 brightness, u32 blink_fade, u32 color_state,
                struct led_set_state_return *retval)
{
        struct led_set_state_args args = {
                .led = led,
                .brightness = brightness,
                .blink_fade = blink_fade,
                .color_state = color_state
        };

        struct acpi_buffer input;
        struct acpi_buffer output = { ACPI_ALLOCATE_BUFFER, NULL };
        acpi_status status;
        union acpi_object *obj;

        input.length = (acpi_size) sizeof(args);
        input.pointer = &args;
        
	// Per Intel docs, first instance is used (instance is indexed from 0)
        status = wmi_evaluate_method(NUCLED_WMI_MGMT_GUID, 0, NUCLED_WMI_METHODID_SETSTATE,
                                     &input, &output);

        if (ACPI_FAILURE(status))
	{
		ACPI_EXCEPTION((AE_INFO, status, "wmi_evaluate_method"));
                return -EIO;
	}

        // Always returns a buffer
        obj = (union acpi_object *)output.pointer;
        if (obj && retval)
        {
                retval->brightness_return = obj->buffer.pointer[0];
                retval->blink_fade_return = obj->buffer.pointer[1];
                retval->color_return      = obj->buffer.pointer[2];
        }

        kfree(obj);

        return 0;
}

static ssize_t acpi_proc_write(struct file *filp, const char __user *buff,
                size_t len, loff_t *data)
{
        int i = 0;
        int ret = 0;
        char *input, *arg, *sep;
        static int status  = 0;
        struct led_set_state_return retval;
        u32 led, brightness, blink_fade, color_state;

        // Move buffer from user space to kernel space
        input = vmalloc(len);
        if (!input)
                return -ENOMEM;

        if (copy_from_user(input, buff, len))
                return -EFAULT;

        // Strip new line
        input[len] = '\0';
        if (input[len - 1] == '\n')
                input[len - 1] = '\0';

        // Parse input string
	sep = input;
        while ((arg = strsep(&sep, ",")) && *arg)
        {
                if (i == 0)             // First arg: LED ("power" or "ring")
                {
                        if (!strcmp(arg, "power"))
                                led = NUCLED_WMI_POWER_LED_ID;
                        else if (!strcmp(arg, "ring"))
                                led = NUCLED_WMI_RING_LED_ID;
                        else
                                ret = -EINVAL;
                }
                else if (i == 1)        // Second arg: brightness (0 - 100)
                {
                        long val;

                        if (kstrtol(arg, 0, &val))
                        {
                                ret = -EINVAL;
                        }
                        else
                        {
                                if (val < 0 || val > 100)
                                        ret = -EINVAL;
                                else
                                        brightness = val;
                        }
                }
                else if (i == 2)        // Third arg: fade/brightness (text values)
                {
                        if (!strcmp(arg, "none"))
                                blink_fade = NUCLED_WMI_ALWAYS_ON;
                        else if (!strcmp(arg, "blink_fast"))
                                blink_fade = NUCLED_WMI_BLINK_1HZ;
                        else if (!strcmp(arg, "blink_medium"))
                                blink_fade = NUCLED_WMI_BLINK_0_5HZ;
                        else if (!strcmp(arg, "blink_slow"))
                                blink_fade = NUCLED_WMI_BLINK_0_25HZ;
                        else if (!strcmp(arg, "fade_fast"))
                                blink_fade = NUCLED_WMI_FADE_1HZ;
                        else if (!strcmp(arg, "fade_medium"))
                                blink_fade = NUCLED_WMI_FADE_0_5HZ;
                        else if (!strcmp(arg, "fade_slow"))
                                blink_fade = NUCLED_WMI_FADE_0_25HZ;
                        else
                                ret = -EINVAL;
                }
                else if (i == 3)        // Fourth arg: color (text values)
                {
                        if (led == NUCLED_WMI_POWER_LED_ID)
                        {
                                if (!strcmp(arg, "off"))
                                        color_state = NUCLED_WMI_POWER_COLOR_DISABLE;
                                else if (!strcmp(arg, "blue"))
                                        color_state = NUCLED_WMI_POWER_COLOR_BLUE;
                                else if (!strcmp(arg, "amber"))
                                        color_state = NUCLED_WMI_POWER_COLOR_AMBER;
                                else
                                        ret = -EINVAL;
                        }
                        else if (led == NUCLED_WMI_RING_LED_ID)
                        {
                                if (!strcmp(arg, "off"))
                                        color_state = NUCLED_WMI_RING_COLOR_DISABLE;
                                else if (!strcmp(arg, "cyan"))
                                        color_state = NUCLED_WMI_RING_COLOR_CYAN;
                                else if (!strcmp(arg, "pink"))
                                        color_state = NUCLED_WMI_RING_COLOR_PINK;
                                else if (!strcmp(arg, "yellow"))
                                        color_state = NUCLED_WMI_RING_COLOR_YELLOW;
                                else if (!strcmp(arg, "blue"))
                                        color_state = NUCLED_WMI_RING_COLOR_BLUE;
                                else if (!strcmp(arg, "red"))
                                        color_state = NUCLED_WMI_RING_COLOR_RED;
                                else if (!strcmp(arg, "green"))
                                        color_state = NUCLED_WMI_RING_COLOR_GREEN;
                                else if (!strcmp(arg, "white"))
                                        color_state = NUCLED_WMI_RING_COLOR_WHITE;
                                else
                                        ret = -EINVAL;
                        }
                }
                else                    // Too many args!
                        ret = -EOVERFLOW;

                // Track iterations
                i++;
        }

        vfree(input);

        if (ret == -EOVERFLOW)
        {
                pr_warn("Too many arguments while setting NUC LED state\n");
        }
        else if (i != 4)
        {
                pr_warn("Too few arguments while setting NUC LED state\n");
        }
        else if (ret == -EINVAL)
        {
                pr_warn("Invalid argument while setting NUC LED state\n");
        }
        else
        {
                status = nuc_led_set_state(led, brightness, blink_fade, color_state, &retval);
                if (status)
                {
                        pr_warn("Unable to set NUC LED state: WMI call failed\n");
                }
                else
                {
                        if (retval.brightness_return == NUCLED_WMI_RETURN_UNDEFINED)
                        {
                                if (led == NUCLED_WMI_POWER_LED_ID)
                                        pr_warn("Unable set NUC power LED state: not set for SW control\n");
                                else if (led == NUCLED_WMI_RING_LED_ID)
                                        pr_warn("Unable set NUC ring LED state: not set for SW control\n");
                        }
                        else if (retval.brightness_return == NUCLED_WMI_RETURN_BADPARAM || retval.blink_fade_return == NUCLED_WMI_RETURN_BADPARAM ||
                                 retval.color_return == NUCLED_WMI_RETURN_BADPARAM)
                        {
                                pr_warn("Unable to set NUC LED state: invalid parameter\n");
                        }
                        else if (retval.brightness_return != NUCLED_WMI_RETURN_SUCCESS)
                        {
                                pr_warn("Unable to set NUC LED state: WMI call returned error\n");
                        }
                }
        }

        return len;
}

static ssize_t acpi_proc_read(struct file *filp, char __user *buff,
                size_t count, loff_t *off)
{
        ssize_t ret;
        static int status_pwr  = 0;
        static int status_ring = 0;
        struct led_get_state_return power_led;
        struct led_get_state_return ring_led;
        int len = 0;

        // Get statuses from WMI interface
        status_pwr = nuc_led_get_state(NUCLED_WMI_POWER_LED_ID, &power_led);
        if (status_pwr)
                pr_warn("Unable to get NUC power LED state\n");

        status_ring = nuc_led_get_state(NUCLED_WMI_RING_LED_ID, &ring_led);
        if (status_ring)
                pr_warn("Unable to get NUC ring LED state\n");

        // Clear buffer
        memset(result_buffer, 0, BUFFER_SIZE);

        // Process state for power LED
        if (status_pwr)
        {
                sprintf(get_buffer_end(), "Power LED state could not be determined: WMI call failed\n\n");
        }
        else
        {
                if (power_led.return_code == NUCLED_WMI_RETURN_SUCCESS)
                        sprintf(get_buffer_end(), "Power LED Brightness: %d%%\nPower LED Blink/Fade: %s (0x%02x)\nPower LED Color: %s (0x%02x)\n\n",
                                power_led.brightness,
                                blink_fade_text[power_led.blink_fade], power_led.blink_fade,
                                pwrcolor_text[power_led.color_state], power_led.color_state);
                else if (power_led.return_code == NUCLED_WMI_RETURN_UNDEFINED)
                        sprintf(get_buffer_end(), "Power LED not set for software control\n\n");
                else
                        sprintf(get_buffer_end(), "Power LED state could not be determined: WMI call returned error\n\n");
        }

        // Process state for ring LED
        if (status_ring)
        {
                sprintf(get_buffer_end(), "Ring LED state could not be determined: WMI call failed\n\n");
        }
        else
        {
                if (ring_led.return_code == NUCLED_WMI_RETURN_SUCCESS)
                        sprintf(get_buffer_end(), "Ring LED Brightness: %d%%\nRing LED Blink/Fade: %s (0x%02x)\nRing LED Color: %s (0x%02x)\n\n",
                                ring_led.brightness,
                                blink_fade_text[ring_led.blink_fade], ring_led.blink_fade,
                                ringcolor_text[ring_led.color_state], ring_led.color_state);
                else if (power_led.return_code == NUCLED_WMI_RETURN_UNDEFINED)
                        sprintf(get_buffer_end(), "Ring LED not set for software control\n\n");
                else
                        sprintf(get_buffer_end(), "Ring LED state could not be determined: WMI call returned error\n\n");
        }

        // Return buffer via proc
        len = strlen(result_buffer);
        ret = simple_read_from_buffer(buff, count, off, result_buffer, len + 1);

        return ret;
}

static struct proc_ops proc_acpi_operations = {
        .proc_read     = acpi_proc_read,
        .proc_write    = acpi_proc_write,
};

/* Init & unload */
static int __init init_nuc_led(void)
{
        struct proc_dir_entry *acpi_entry;
	kuid_t uid;
	kgid_t gid;

        // Make sure LED control WMI GUID exists
        if (!wmi_has_guid(NUCLED_WMI_MGMT_GUID)) {
                pr_warn("Intel NUC LED WMI GUID not found\n");
                return -ENODEV;
        }

        // Verify the user parameters
	uid = make_kuid(&init_user_ns, nuc_led_uid);
	gid = make_kgid(&init_user_ns, nuc_led_gid);

	if (!uid_valid(uid) || !gid_valid(gid)) {
                pr_warn("Intel NUC LED control driver got an invalid UID or GID\n");
		return -EINVAL;
	}

        // Create nuc_led ACPI proc entry
        acpi_entry = proc_create("nuc_led", nuc_led_perms, acpi_root_dir, &proc_acpi_operations);

        if (acpi_entry == NULL) {
                pr_warn("Intel NUC LED control driver could not create proc entry\n");
                return -ENOMEM;
        }

        proc_set_user(acpi_entry, uid, gid);

        pr_info("Intel NUC LED control driver loaded\n");

        return 0;
}

static void __exit unload_nuc_led(void)
{
        remove_proc_entry("nuc_led", acpi_root_dir);
        pr_info("Intel NUC LED control driver unloaded\n");
}

module_init(init_nuc_led);
module_exit(unload_nuc_led);
