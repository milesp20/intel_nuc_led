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
#include <linux/notifier.h>
#include <linux/reboot.h>

#include "nuc_led.h"

MODULE_AUTHOR("Miles Peterson");
MODULE_DESCRIPTION("Intel NUC LED Control WMI Driver");
MODULE_LICENSE("GPL");
ACPI_MODULE_NAME("NUC_LED");

static int turn_off_led(struct notifier_block *, unsigned long, void *);

static struct notifier_block nb = {
	.notifier_call = turn_off_led
};

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
        if (!input){
                return -ENOMEM;
        }

        if (copy_from_user(input, buff, len)){
                return -EFAULT;
        }

        // Strip new line
        input[len] = '\0';
        if (input[len - 1] == '\n'){
                input[len - 1] = '\0';
        }

        // Parse input string
	sep = input;
        while ((arg = strsep(&sep, ",")) && *arg)
        {
                switch (i) {
                case 0: // First arg: LED ("power" or "ring")
                        if (!strcmp(arg, "power"))
                                led = NUCLED_WMI_POWER_LED_ID;
                        else if (!strcmp(arg, "ring"))
                                led = NUCLED_WMI_RING_LED_ID;
                        else
                                ret = -EINVAL;
                        break;

                case 1: // Second arg: brightness (0 - 100)
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
                        break;
                        }

                case 2: // Third arg: fade/brightness (text values)
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
                        break;

                case 3: // Fourth arg: color (text values)
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
                        break;
                default: // Too many args!
                        ret = -EOVERFLOW;
                }
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

static void print_power_state_to_buffer(int status_pwr, struct led_get_state_return power_led){
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
}

static void print_ring_state_to_buffer(int status_ring, struct led_get_state_return ring_led){
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
          else if (ring_led.return_code == NUCLED_WMI_RETURN_UNDEFINED)
                  sprintf(get_buffer_end(), "Ring LED not set for software control\n\n");
          else
                  sprintf(get_buffer_end(), "Ring LED state could not be determined: WMI call returned error\n\n");
  }
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
        print_power_state_to_buffer(status_pwr, power_led);

        // Process state for ring LED
        print_ring_state_to_buffer(status_ring, ring_led);

        // Return buffer via proc
        len = strlen(result_buffer);
        ret = simple_read_from_buffer(buff, count, off, result_buffer, len + 1);

        return ret;
}

static struct file_operations proc_acpi_operations = {
        .owner    = THIS_MODULE,
        .read     = acpi_proc_read,
        .write    = acpi_proc_write,
};

/* Turn off all LEDs */
static int turn_off_led(struct notifier_block *nb, unsigned long action, void *data){
        struct led_get_state_return power_led;
        struct led_get_state_return ring_led;
        static int status_pwr  = 0;
        static int status_ring = 0;

        struct led_set_state_return retval;

        // Try and get LED status then set brightness to 0 while maintaining other settings
        // If this fails we're unlikely to be able to set LED state at all
        // but we attempt to set it to a completely off state.
        status_pwr = nuc_led_get_state(NUCLED_WMI_POWER_LED_ID, &power_led);
        if (status_pwr){
                pr_warn("Unable to get NUC power LED state\n");
                nuc_led_set_state(NUCLED_WMI_POWER_LED_ID, 0, NUCLED_WMI_ALWAYS_ON, NUCLED_WMI_POWER_COLOR_DISABLE,
                            &retval);
        } else{
                nuc_led_set_state(NUCLED_WMI_POWER_LED_ID, 0, power_led.blink_fade, power_led.color_state,
                            &retval);
        }

        status_ring = nuc_led_get_state(NUCLED_WMI_RING_LED_ID, &ring_led);
        if (status_ring){
                pr_warn("Unable to get NUC ring LED state\n");
                nuc_led_set_state(NUCLED_WMI_RING_LED_ID, 0, NUCLED_WMI_ALWAYS_ON, NUCLED_WMI_RING_COLOR_DISABLE,
                            &retval);
        } else{
                nuc_led_set_state(NUCLED_WMI_RING_LED_ID, 0, ring_led.blink_fade, ring_led.color_state,
                            &retval);
        }

        return NOTIFY_OK;
}

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

        register_reboot_notifier(&nb);

        pr_info("Intel NUC LED control driver loaded\n");

        return 0;
}

static void __exit unload_nuc_led(void)
{
        unregister_reboot_notifier(&nb);
        remove_proc_entry("nuc_led", acpi_root_dir);
        pr_info("Intel NUC LED control driver unloaded\n");
}

module_init(init_nuc_led);
module_exit(unload_nuc_led);
