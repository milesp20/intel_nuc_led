
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
