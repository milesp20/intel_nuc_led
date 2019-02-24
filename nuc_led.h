// Intel NUC WMI GUID:
#define NUCLED_WMI_MGMT_GUID            "8C5DA44C-CDC3-46b3-8619-4E26D34390B7"
MODULE_ALIAS("wmi:" NUCLED_WMI_MGMT_GUID);

// LED Control Method ID:
#define NUCLED_WMI_METHODID_GETSTATE    0x01
#define NUCLED_WMI_METHODID_SETSTATE    0x02

// LED Identifiers:
#define NUCLED_WMI_POWER_LED_ID         0x01
#define NUCLED_WMI_RING_LED_ID          0x02

// Return codes:
#define NUCLED_WMI_RETURN_SUCCESS       0x00
#define NUCLED_WMI_RETURN_NOSUPPORT     0xE1
#define NUCLED_WMI_RETURN_UNDEFINED     0xE2
#define NUCLED_WMI_RETURN_NORESPONSE    0xE3
#define NUCLED_WMI_RETURN_BADPARAM      0xE4
#define NUCLED_WMI_RETURN_UNEXPECTED    0xEF

// Blink and fade:
#define NUCLED_WMI_BLINK_1HZ            0x01
#define NUCLED_WMI_BLINK_0_25HZ         0x02
#define NUCLED_WMI_FADE_1HZ             0x03
#define NUCLED_WMI_ALWAYS_ON            0x04
#define NUCLED_WMI_BLINK_0_5HZ          0x05
#define NUCLED_WMI_FADE_0_25HZ          0x06
#define NUCLED_WMI_FADE_0_5HZ           0x07

// Power button colors:
#define NUCLED_WMI_POWER_COLOR_DISABLE  0x00
#define NUCLED_WMI_POWER_COLOR_BLUE     0x01
#define NUCLED_WMI_POWER_COLOR_AMBER    0x02

// Ring colors:
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
        int32_t  return_code;
        int32_t  brightness;
        int32_t  blink_fade;
        int32_t  color_state;
} __packed;

struct led_set_state_args {
        u8 led;
        u8 brightness;
        u8 blink_fade;
        u8 color_state;
}__packed;

struct led_set_state_return {
        int32_t  brightness_return;
        int32_t  blink_fade_return;
        int32_t  color_return;
} __packed;

#define BUFFER_SIZE 512
static char result_buffer[BUFFER_SIZE];
static char *get_buffer_end(void) {
    return result_buffer + strlen(result_buffer);
}

// Convert blink/fade value to text:
static const char* const blink_fade_text[] = { "Current", "Solid", "1Hz Blink", "0.25Hz Blink", "1Hz Fade", "Always On", "0.5Hz Blink", "0.25Hz Fade", "0.5Hz Fade", "Current" };

// Convert color value to text:
static const char* const pwrcolor_text[] =   { "Current", "Off", "Blue", "Amber" };
static const char* const ringcolor_text[] =  { "Current", "Off", "Cyan", "Pink", "Yellow", "Blue", "Red", "Green", "White" };

// "Current setting" flag for profiles:
#define NUCLED_CURRENT_SETTING          -1

// Profile IDs:
#define NUCLED_PROFILE_CURRENT          0x00
#define NUCLED_PROFILE_BOOT             0x01
#define NUCLED_PROFILE_SHUTDOWN         0x02
#define NUCLED_PROFILE_SUSPEND          0x03
#define NUCLED_PROFILE_WAKE             0x04
#define NUCLED_PROFILE_HIBERNATE        0x05
#define NUCLED_PROFILE_RESTORE          0x06
#define NUCLED_PROFILE_RECORDING        0x07
#define NUCLED_PROFILE_VOICE            0x08
#define NUCLED_MAX_PROFILES             NUCLED_PROFILE_VOICE + 1

// Profile storage area:
struct led_get_state_return power_profile[ NUCLED_MAX_PROFILES ] = {
	/* Profile: Current */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Boot */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Shutdown */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Suspend */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Wake */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Hibernate */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Restore */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Recording */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Voice */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	}
};
struct led_get_state_return ring_profile[ NUCLED_MAX_PROFILES ] = {
	/* Profile: Current */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Boot */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Shutdown */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Suspend */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Wake */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Hibernate */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Restore */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Recording */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	},
	/* Voice */
	{
		.brightness = NUCLED_CURRENT_SETTING,
		.blink_fade = NUCLED_CURRENT_SETTING,
		.color_state = NUCLED_CURRENT_SETTING
	}
};
static const char* const profile_name[] = { "current", "boot", "shutdown", "suspend", "wake", "hibernate", "restore", "recording", "voice" };
static int profile_id = NUCLED_PROFILE_CURRENT;
static int is_module_busy = false;

// Profile handlers:
static int profiles_op_read_handler(char *buffer, const struct kernel_param *kp);
static int profiles_op_write_handler(const char *buffer, const struct kernel_param *kp);
static const struct kernel_param_ops profiles_op = {
	.get = profiles_op_read_handler,
	.set = profiles_op_write_handler
};

// Module parameter storage:
static unsigned int nuc_led_perms __read_mostly = S_IRUGO | S_IWUSR | S_IWGRP;
static unsigned int nuc_led_uid __read_mostly;
static unsigned int nuc_led_gid __read_mostly;
static int debug = false;
static int hibernate_same = true;

// Module parameter definitions and descriptions:
module_param(debug, uint, S_IRUGO | S_IWUSR | S_IWGRP);
module_param(hibernate_same, uint, S_IRUGO | S_IWUSR | S_IWGRP);
module_param(nuc_led_perms, uint, 0);
module_param(nuc_led_uid, uint, 0);
module_param(nuc_led_gid, uint, 0);
module_param_cb(nuc_led_profiles, &profiles_op, NULL, S_IRUGO | S_IWUSR | S_IWGRP);

MODULE_PARM_DESC(debug, "flag to allow more information to be displayed by dmesg");
MODULE_PARM_DESC(hibernate_same, "flag to treat hibernate and suspend as same event");
MODULE_PARM_DESC(nuc_led_perms, "permissions on /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_uid, "default owner of /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_gid, "default group of /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_profiles, "LED information for profile states");
