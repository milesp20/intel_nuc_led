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
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
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
#include <linux/suspend.h>
#include <linux/unistd.h>
#include "nuc_led.h"

MODULE_AUTHOR("Miles Peterson");
MODULE_DESCRIPTION("Intel NUC LED Control WMI Driver");
MODULE_LICENSE("GPL");
ACPI_MODULE_NAME("NUC_LED");

/******************************************************************************/
// Functions to control the LED states:
/******************************************************************************/
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
	status = wmi_evaluate_method(NUCLED_WMI_MGMT_GUID, 0, NUCLED_WMI_METHODID_GETSTATE, &input, &output);

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
static int nuc_led_set_state(u32 led, u32 brightness, u32 blink_fade, u32 color_state, struct led_set_state_return *retval)
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
	status = wmi_evaluate_method(NUCLED_WMI_MGMT_GUID, 0, NUCLED_WMI_METHODID_SETSTATE, &input, &output);

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

/******************************************************************************/
// Function that changes specifed LED to specified profile state
/******************************************************************************/
static void nuc_led_change_profile(int which, struct led_get_state_return *p)
{
	struct led_get_state_return *led;

	// Just skip this if no changes are required:
	if (p)
	{
		if (p->brightness == NUCLED_CURRENT_SETTING && p->blink_fade == NUCLED_CURRENT_SETTING && p->color_state == NUCLED_CURRENT_SETTING)
			return;

		// Determine which "led state" structure to use:
		if (which == NUCLED_WMI_POWER_LED_ID)
			led = &power_profile[ NUCLED_PROFILE_CURRENT ];
		else
			led = &ring_profile[ NUCLED_PROFILE_CURRENT ];

		if (!led || (led->brightness == NUCLED_CURRENT_SETTING && led->blink_fade == NUCLED_CURRENT_SETTING && led->color_state == NUCLED_CURRENT_SETTING))
			return;

		// Decide what the current state should be:
		led->brightness = (p->brightness > NUCLED_CURRENT_SETTING ? p->brightness : led->brightness);
		led->blink_fade = (p->blink_fade > NUCLED_CURRENT_SETTING ? p->blink_fade : led->blink_fade);
		led->color_state = (p->color_state > NUCLED_CURRENT_SETTING ? p->color_state : led->color_state);

		// Set the power LED to the profile specified:
		nuc_led_set_state(which, led->brightness, led->blink_fade, led->color_state, NULL);
	}
}

/******************************************************************************/
// Functions responsable for input:
/******************************************************************************/
static void nuc_led_set_profile(struct led_get_state_return *p, int brightness, int blink_fade, int color_state)
{
	if (p)
	{
		p->brightness = brightness;
		p->blink_fade = blink_fade;
		p->color_state = color_state;
	}
}

static ssize_t nuc_led_parse_input(char *input, ssize_t len)
{
	int i = 0;
	int ret = 0;
	char *arg, *sep;
	struct led_set_state_return retval;
	u32 led = 0, brightness = 0, blink_fade = 0, color_state = 0;
	long val;
	int set_profile = false;
	int view_flag = false;
	struct led_get_state_return *cstate;
	struct led_get_state_return bstate;

	// Reset profile ID to the "current" profile:
	profile_id = NUCLED_PROFILE_CURRENT;

	if (debug)
		printk("[%d] arg = %s", __LINE__, input);

	// Parse input string
	sep = input;
	while ((arg = strsep(&sep, ",")) && *arg)
	{
		switch (i)
		{
			case 0: // First arg: LED ("power", "ring") or operation ("profile", "view")
				if (!strcmp(arg, "power"))
					led = NUCLED_WMI_POWER_LED_ID;
				else if (!strcmp(arg, "ring"))
					led = NUCLED_WMI_RING_LED_ID;
				else if (len && !strcmp(arg, "profile"))
				{
					i = 3;
					set_profile = true;
				}
				else if (len && !strcmp(arg, "view"))
				{
					i = 3;
					view_flag = true;
				}
				else if (kstrtol(arg, 0, &val))
				{
					if (debug)
						printk(KERN_WARNING "[1A] Invalid argument 1: %s", arg);
					ret = -EINVAL;
				}
				else
				{
					if (val != NUCLED_WMI_POWER_LED_ID && val != NUCLED_WMI_RING_LED_ID)
					{
						if (debug)
							printk(KERN_WARNING "[1B] Invalid argument 1: %s", arg);
						ret = -EINVAL;
					}
					else
						led = val;
				}
				break;

			case 1: // Second arg: brightness (-1 to 100, or "current")
				if (!strcmp(arg, "current"))
					brightness = NUCLED_CURRENT_SETTING;
				else if (kstrtol(arg, 0, &val))
				{
					if (debug)
						printk(KERN_WARNING "[2A] Invalid argument 2: %s", arg);
					ret = -EINVAL;
				}
				else
				{
					if (val == NUCLED_CURRENT_SETTING)
						brightness = NUCLED_CURRENT_SETTING;
					else if (val < 0 || val > 100)
					{
						if (debug)
							printk(KERN_WARNING "[2B] Invalid argument 2: %s", arg);
						ret = -EINVAL;
					}
					else
						brightness = val;
				}
				break;

			case 2: // Third arg: fade/brightness (text or numeric values)
				if (!strcmp(arg, "none") || !strcmp(arg, "solid") || !strcmp(arg, "off"))
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
				else if (!strcmp(arg, "current"))
					blink_fade = NUCLED_CURRENT_SETTING;
				else if (kstrtol(arg, 0, &val))
				{
					if (debug)
						printk(KERN_WARNING "[3A] Invalid argument 3: %s", arg);
					ret = -EINVAL;
				}
				else
				{
					if (val < NUCLED_CURRENT_SETTING || val > NUCLED_WMI_FADE_0_25HZ)
					{
						if (debug)
							printk(KERN_WARNING "[3B] Invalid argument 3: %s", arg);
						ret = -EINVAL;
					}
					else
						blink_fade = val;
				}
				break;

			case 3: // Fourth arg: color (text or numeric values)
				if (led == NUCLED_WMI_POWER_LED_ID)
				{
					if (!strcmp(arg, "off"))
						color_state = NUCLED_WMI_POWER_COLOR_DISABLE;
					else if (!strcmp(arg, "blue"))
						color_state = NUCLED_WMI_POWER_COLOR_BLUE;
					else if (!strcmp(arg, "amber"))
						color_state = NUCLED_WMI_POWER_COLOR_AMBER;
					else if (!strcmp(arg, "current"))
						color_state = NUCLED_CURRENT_SETTING;
					else if (kstrtol(arg, 0, &val))
					{
						if (debug)
							printk(KERN_WARNING "[4A-P] Invalid argument 4: %s", arg);
						ret = -EINVAL;
					}
					else
					{
						if (val < NUCLED_CURRENT_SETTING || val > 100)
						{
							if (debug)
								printk(KERN_WARNING "[4B-P] Invalid argument 4: %s", arg);
							ret = -EINVAL;
						}
						else
							color_state = val;
					}
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
					else if (!strcmp(arg, "current"))
						color_state = NUCLED_CURRENT_SETTING;
					else if (kstrtol(arg, 0, &val))
					{
						if (debug)
							printk(KERN_WARNING "[4A-R] Invalid argument 5: %s", arg);
						ret = -EINVAL;
					}
					else
					{
						if (val < NUCLED_CURRENT_SETTING || val > 100)
						{
							if (debug)
								printk(KERN_WARNING "[4B-R] Invalid argument 4: %s", arg);
							ret = -EINVAL;
						}
						else
							color_state = val;
					}
				}
				break;

			case 4: // Optional fifth arg: Profile name (text only)
				profile_id = NUCLED_CURRENT_SETTING;
				for (val = NUCLED_PROFILE_CURRENT; val < NUCLED_MAX_PROFILES; val++)
				{
					if (!strcmp(arg, profile_name[val]))
						profile_id = val;
				}
				if (profile_id == NUCLED_CURRENT_SETTING)
				{
					if (kstrtol(arg, 0, &val))
					{
						if (debug)
							printk(KERN_WARNING "[5A] Invalid argument 5: %s", arg);
						ret = -EINVAL;
					}
					else
					{
						if (val < NUCLED_PROFILE_CURRENT || val >= NUCLED_MAX_PROFILES)
						{
							if (debug)
								printk(KERN_WARNING "[5B] Invalid argument 5: %s", arg);
							ret = -EINVAL;
						}
						else
							profile_id = val;
					}
				}
				break;

			default: // Too many args!
				ret = -EOVERFLOW;
		}

		// Track iterations
		i++;
		if (ret)
			break;
	}

	if (ret == -EOVERFLOW)
	{
		pr_warn("Too many arguments while setting NUC LED state\n");
		profile_id = NUCLED_PROFILE_CURRENT;
	}
	else if (ret == -EINVAL)
	{
		if (!debug)
			pr_warn("Invalid arguments while setting NUC LED state\n");
		profile_id = NUCLED_PROFILE_CURRENT;
	}
	else if (profile_id == NUCLED_PROFILE_CURRENT && (i < 4 || i > 5))
	{
		pr_warn("Too few arguments while setting NUC LED state\n");
		profile_id = NUCLED_PROFILE_CURRENT;
		ret = -EINVAL;
	}
	else if (profile_id != NUCLED_PROFILE_CURRENT && i != 5)
	{
		pr_warn("Too few arguments while setting NUC LED state\n");
		profile_id = NUCLED_PROFILE_CURRENT;
		ret = -EINVAL;
	}
	else if (set_profile)
	{
		nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ profile_id ] );
		nuc_led_change_profile( NUCLED_WMI_RING_LED_ID, &ring_profile[ profile_id ] );
		profile_id = NUCLED_PROFILE_CURRENT;
	}
	else if (view_flag)
	{
		// Nothing more to do.....  Profile ID is set for next read!
		// WARNING: DO NOT DELETE THIS BLOCK!  This block is required and
		// very important to have so that next block(s) don't get executed!!!
	}
	else if (profile_id != NUCLED_PROFILE_CURRENT)
	{
		if (!nuc_led_get_state(led, &bstate) && bstate.return_code == NUCLED_WMI_RETURN_SUCCESS)
		{
			// Set the profile to the settings requested
			if (led == NUCLED_WMI_POWER_LED_ID)
				nuc_led_set_profile(&power_profile[ profile_id ], brightness, blink_fade, color_state);
			else
				nuc_led_set_profile(&ring_profile[ profile_id ], brightness, blink_fade, color_state);
		}

		// Reset profile ID for next boot
		profile_id = NUCLED_PROFILE_CURRENT;
	}
	else
	{
		// Determine which "led state" structure to use:
		if (led == NUCLED_WMI_POWER_LED_ID)
			cstate = &power_profile[ NUCLED_PROFILE_CURRENT ];
		else
			cstate = &ring_profile[ NUCLED_PROFILE_CURRENT ];

		// Decide what the current state should be:
		if (cstate && cstate->brightness != NUCLED_CURRENT_SETTING)
		{
			brightness = (brightness == NUCLED_CURRENT_SETTING ? cstate->brightness : brightness);
			blink_fade = (blink_fade == NUCLED_CURRENT_SETTING ? cstate->blink_fade : blink_fade);
			color_state = (color_state == NUCLED_CURRENT_SETTING ? cstate->color_state : color_state);
		}

		// Try to set the requested state and report whether successful or not:
		if (nuc_led_set_state(led, brightness, blink_fade, color_state, &retval))
		{
			pr_warn("Unable to set NUC LED state: WMI call failed\n");
		}
		else
		{
			if (retval.brightness_return == NUCLED_WMI_RETURN_SUCCESS)
			{
				nuc_led_set_profile(cstate, brightness, blink_fade, color_state);
			}
			else if (retval.brightness_return == NUCLED_WMI_RETURN_UNDEFINED)
			{
				if (led == NUCLED_WMI_POWER_LED_ID)
					pr_warn("Unable set NUC power LED state: not set for SW control\n");
				else if (led == NUCLED_WMI_RING_LED_ID)
					pr_warn("Unable set NUC ring LED state: not set for SW control\n");
			}
			else if (retval.brightness_return == NUCLED_WMI_RETURN_BADPARAM || retval.brightness_return == NUCLED_WMI_RETURN_BADPARAM ||
				 retval.brightness_return == NUCLED_WMI_RETURN_BADPARAM)
			{
				pr_warn("Unable to set NUC LED state: invalid parameter\n");
			}
			else if (retval.brightness_return != NUCLED_WMI_RETURN_SUCCESS)
			{
				pr_warn("Unable to set NUC LED state: WMI call returned error\n");
			}
		}
	}

	return (ret ? ret : len);
}

static ssize_t acpi_proc_write(struct file *filp, const char __user *buff, size_t len, loff_t *data)
{
	int ret = 0;
	size_t max = BUFFER_SIZE - 1;

	// If module is already busy, abort with error:
	if (is_module_busy)
		return -EBUSY;
	is_module_busy = true;

	// Clear the result buffer, then copy the user buffer into it:
	len = min(max, len);
	memset(result_buffer, 0, BUFFER_SIZE);
	ret = copy_from_user(result_buffer, buff, len);
	if (ret)
	{
		if (debug)
			printk("Result from copy_from_user = %d", ret);
		return -EFAULT;
	}

	// Strip new line
	result_buffer[len] = '\0';
	if (result_buffer[len - 1] == '\n')
		result_buffer[len - 1] = '\0';

	// Call the parsing function to actually parse the string:
	ret = nuc_led_parse_input(result_buffer, len);
	is_module_busy = false;
	return ret;
}

/******************************************************************************/
// Functions responsible for outputting human-readable status of LEDs:
/******************************************************************************/
static void nuc_led_print_readable(int led, struct led_get_state_return *profile, char *s)
{
	struct led_get_state_return state;

	if (profile)
	{
		if (nuc_led_get_state(led, &state))
		{
			printk("%s state: WMI call failed.  Unable to read state.\n", s);
			sprintf(get_buffer_end(), "%s state state could not be determined: WMI call failed\n\n", s);
		}
		else
		{
			if (state.return_code == NUCLED_WMI_RETURN_SUCCESS)
			{
				if (profile_id == NUCLED_PROFILE_CURRENT)
					*profile = state;
				sprintf(get_buffer_end(), "%s state Brightness: %d%%\n%s state Blink/Fade: %s\n%s state Color: %s\n\n",
					s, profile->brightness,
					s, blink_fade_text[profile->blink_fade + 1],
					s, !strcmp(s, "Power") ? pwrcolor_text[profile->color_state + 1] : ringcolor_text[profile->color_state + 1]);
			}
			else if (state.return_code == NUCLED_WMI_RETURN_UNDEFINED)
				sprintf(get_buffer_end(), "%s state not set for software control\n\n", s);
			else
				sprintf(get_buffer_end(), "%s state state could not be determined: WMI call returned error\n\n", s);
		}
	}
}

static ssize_t acpi_proc_read(struct file *filp, char __user *buff,	size_t count, loff_t *off)
{
	ssize_t ret;
	int len = 0;
	char *old_end;

	// If module is already busy, abort with error:
	if (is_module_busy)
		return -EBUSY;
	is_module_busy = true;

	// Clear buffer
	memset(result_buffer, 0, BUFFER_SIZE);

	// Display profile name:
	sprintf(get_buffer_end(), "Profile: ");
	old_end = get_buffer_end();
	sprintf(old_end, "%s\n==================================================\n", profile_name[ profile_id ]);
	*old_end = toupper(*old_end);

	// Get power status from WMI interface
	nuc_led_print_readable(NUCLED_WMI_POWER_LED_ID, &power_profile[ profile_id ], "Power");

	// Get ring status from WMI interface
	nuc_led_print_readable(NUCLED_WMI_RING_LED_ID, &ring_profile[ profile_id ], "Ring");

	// Reset everything for next module read:
	profile_id = NUCLED_PROFILE_CURRENT;

	// Return buffer via proc
	len = strlen(result_buffer);
	ret = simple_read_from_buffer(buff, count, off, result_buffer, len + 1);
	is_module_busy = false;
	return ret;
}

static struct file_operations proc_acpi_operations = {
	.owner    = THIS_MODULE,
	.read     = acpi_proc_read,
	.write    = acpi_proc_write,
};

/******************************************************************************/
// Functions dealing with multiple profile reading and setting at one time:
/******************************************************************************/
static void nuc_led_print_profile(int s, struct led_get_state_return *p, int n)
{
	if (p && (p->brightness != NUCLED_CURRENT_SETTING || p->blink_fade != NUCLED_CURRENT_SETTING || p->color_state != NUCLED_CURRENT_SETTING))
		sprintf(get_buffer_end(), "%d,%d,%d,%d,%d;", s, p->brightness, p->blink_fade, p->color_state, n );
}

static int profiles_op_read_handler(char *buffer, const struct kernel_param *kp)
{
	int i, len;

	// If module is already busy, abort with error:
	if (is_module_busy)
		return -EBUSY;
	is_module_busy = true;

	// Clear the result buffer first:
	memset(result_buffer, 0, BUFFER_SIZE);

	// Print all power LED states:
	for (i = NUCLED_PROFILE_BOOT; i < NUCLED_MAX_PROFILES; i++)
		nuc_led_print_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ i ],  i );

	// Print all ring LED states:
	for (i = NUCLED_PROFILE_BOOT; i < NUCLED_MAX_PROFILES; i++)
		nuc_led_print_profile( NUCLED_WMI_RING_LED_ID, &ring_profile[ i ], i );

	// Copy the results to the user buffer and return:
	len = strlen(result_buffer);
	result_buffer[ len - 1] = '\n';
	strncpy(buffer, result_buffer, len + 1);
	is_module_busy = false;
	return len;
}

static int profiles_op_write_handler(const char *buffer, const struct kernel_param *kp)
{
	char *arg, *sep;
	int result, len;

	// If module is already busy, abort with error:
	if (is_module_busy)
		return -EBUSY;
	is_module_busy = true;

	// Clear the result buffer, then copy the user buffer into it:
	memset(result_buffer, 0, BUFFER_SIZE);
	sep = get_buffer_end();
	len = BUFFER_SIZE - 1;
	len = min(len, (int) strlen(buffer));
	strncpy(sep, buffer, len);

	// Strip new line
	result_buffer[len] = '\0';
	if (result_buffer[len - 1] == '\n')
		result_buffer[len - 1] = '\0';

	// Pass each profile string (seperated by semi-colors) to the parser function:
	while ((arg = strsep(&sep, ";")) && *arg)
	{
		if (debug)
			printk("[%d] arg = %s", __LINE__, arg);
		result = nuc_led_parse_input(arg, 0);
		if (result < 0)
			break;
	}
	is_module_busy = false;
	return result;
}

/******************************************************************************/
// Profile change notification functions
/******************************************************************************/
/* Change LED state to shutdown profile */
static int handler_shutdown(struct notifier_block *nb, unsigned long action, void *data)
{
	nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_SHUTDOWN ] );
	nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_SHUTDOWN ] );
	return NOTIFY_OK;
}

static struct notifier_block nb_shutdown = {
	.notifier_call = handler_shutdown
};

/* Change LED state to suspend/wake/hibernate/restore profile */
static int handler_pm(struct notifier_block *nb, unsigned long pm_event, void *data)
{
	switch (pm_event)
	{
		case PM_HIBERNATION_PREPARE:
			// If hibernation and suspend are treated differently, then do this block:
			if (!hibernate_same)
			{
				nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_HIBERNATE ] );
				nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_HIBERNATE ] );
				break;
			}

		case PM_SUSPEND_PREPARE:
			// If hibernation and suspend are treated the same, then do this block:
			nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_SUSPEND ] );
			nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_SUSPEND ] );
			break;

		case PM_RESTORE_PREPARE:
		case PM_POST_HIBERNATION:
			// If post-hibernation and post-suspend are treated differently, then do this block:
			if (!hibernate_same)
			{
				nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_RESTORE ] );
				nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_RESTORE ] );
				break;
			}

		case PM_POST_SUSPEND:
			// If post-hibernation and post-suspend are treated the same, then do this block:
			nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_WAKE ] );
			nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_WAKE ] );
			break;

		default:
			break;
	}
	return NOTIFY_OK;
}

static struct notifier_block nb_pm = {
	.notifier_call = handler_pm
};

/******************************************************************************/
// Module init & unload
/******************************************************************************/
static void nuc_led_get_initial_state(int which, struct led_get_state_return *state)
{
	// Get ring status from WMI interface
	if (state && (nuc_led_get_state(which, state) || state->return_code != NUCLED_WMI_RETURN_SUCCESS))
	{
		state->brightness = NUCLED_CURRENT_SETTING;
		state->blink_fade = NUCLED_CURRENT_SETTING;
		state->color_state = NUCLED_CURRENT_SETTING;
	}
}

static int __init init_nuc_led(void)
{
	struct proc_dir_entry *acpi_entry;
	kuid_t uid;
	kgid_t gid;

	// Make sure LED control WMI GUID exists
	if (!wmi_has_guid(NUCLED_WMI_MGMT_GUID))
	{
		pr_warn("Intel NUC LED WMI GUID not found\n");
		return -ENODEV;
	}

	// Verify the user parameters
	uid = make_kuid(&init_user_ns, nuc_led_uid);
	gid = make_kgid(&init_user_ns, nuc_led_gid);

	if (!uid_valid(uid) || !gid_valid(gid))
	{
		pr_warn("Intel NUC LED control driver got an invalid UID or GID\n");
		return -EINVAL;
	}

	// Create nuc_led ACPI proc entry
	acpi_entry = proc_create("nuc_led", nuc_led_perms, acpi_root_dir, &proc_acpi_operations);
	if (acpi_entry == NULL)
	{
		pr_warn("Intel NUC LED control driver could not create proc entry\n");
		return -ENOMEM;
	}
	proc_set_user(acpi_entry, uid, gid);

	// Register the shutdown and power management notification functions:
	register_reboot_notifier(&nb_shutdown);
	register_pm_notifier(&nb_pm);

	pr_info("Intel NUC LED control driver loaded\n");

	// Get current LED state:
	nuc_led_get_initial_state( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_CURRENT ] );
	nuc_led_get_initial_state( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_CURRENT ] );

	// Change the profile to the default "boot" settings:
	nuc_led_change_profile( NUCLED_WMI_POWER_LED_ID, &power_profile[ NUCLED_PROFILE_BOOT ] );
	nuc_led_change_profile( NUCLED_WMI_RING_LED_ID,  &ring_profile[ NUCLED_PROFILE_BOOT ] );

	return 0;
}

static void __exit unload_nuc_led(void)
{
	// Unregister the notifiers for this module
	unregister_pm_notifier(&nb_pm);
	unregister_reboot_notifier(&nb_shutdown);

	// Remove the "/proc/acpi/nuc_led" entry
	remove_proc_entry("nuc_led", acpi_root_dir);

	pr_info("Intel NUC LED control driver unloaded\n");
}

module_init(init_nuc_led);
module_exit(unload_nuc_led);
