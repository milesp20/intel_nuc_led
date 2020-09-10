"""
nuc_wmi CLI userland for the Intel NUC LED kernel module.
"""

CONTROL_FILE = '/proc/acpi/nuc_led'

LED_BLINK_BEHAVIOR_MULTI_COLOR = {
    0x00: 'Solid',
    0x01: 'Breathing',
    0x02: 'Pulsing',
    0x03: 'Strobing'
}

LED_BLINK_BEHAVIOR_SINGLE_COLOR = {
    0x00: '1Hz',
    0x01: '0.25Hz',
    0x02: '1Hz Fade',
    0x03: '0.25Hz Fade',
    0x04: 'Always On'
}

LED_BLINK_BEHAVIOR = {
    # LED Color Type

    # Dual-color Blue / Amber
    0x00: LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # Dual-color Blue / White
    0x01: LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # RGB-color
    0x02: LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # Single-color LED
    0x03: LED_BLINK_BEHAVIOR_SINGLE_COLOR
}

LED_BLINK_FREEQUENCY = {
    # NUC 7:
    #   - Using BIOS AY0029 or BN0042, only 0x01-0x04 are available.
    #   - Using BIOS AY0038 or BN0043, all frequencies are available.
    'legacy': {
        0x01: '1Hz',
        0x02: '0.25Hz',
        0x03: '1Hz fade',
        0x04: 'Always on',
        0x05: '0.5Hz',
        0x06: '0.25Hz fade',
        0x07: '0.5Hz fade'
    },
    'new': range(0x01, 0x0A)
}

LED_BRIGHTNESS_MULTI_COLOR = range(0x00, 0x64)

LED_BRIGHTNESS_SINGLE_COLOR = {
    0x00: 'OFF',
    0x01: '50%',
    0x02: '100%'
}

LED_BRIGHTNESS = {
    'legacy': LED_BRIGHTNESS_MULTI_COLOR,
    'new': {
        # LED color type

        # Dual-color Blue / Amber
        0x00: LED_BRIGHTNESS_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: LED_BRIGHTNESS_MULTI_COLOR,

        # RGB-color
        0x02: LED_BRIGHTNESS_MULTI_COLOR,

        # Single-color LED
        0x03: LED_BRIGHTNESS_SINGLE_COLOR
    }
}

LED_COLOR = {
    'legacy': {
        'Dual-color Blue / Amber': {
            0x00: 'Disable',
            0x01: 'Blue',
            0x02: 'Amber'
        },
        'RGB-color': {
            0x00: 'Disable',
            0x01: 'Cyan',
            0x02: 'Pink',
            0x03: 'Yellow',
            0x04: 'Blue',
            0x05: 'Red',
            0x06: 'Green',
            0x07: 'White'
        }
    },
    'new': {
        'Dual-color Blue / Amber': {
            0x00: 'Blue',
            0x01: 'Amber'
        },
        'Dual-color Blue / White': {
            0x00: 'Blue',
            0x01: 'White'
        },
        'RGB-color': range(0x00, 0xFF)
    }
}

LED_COLOR_TYPE = {
    'legacy': {
        'S0 Power LED': 'Dual-color Blue / Amber',
        'S0 Ring LED': 'RGB-color'
    },
    'new': {
        0x00: 'Dual-color Blue / Amber',
        0x01: 'Dual-color Blue / White',
        0x02: 'RGB-color',
        0x03: 'Single-color LED'
    }
}

LED_INDICATOR_OPTION = {
    0x00: 'Power State Indicator',
    0x01: 'HDD Activity Indicator',
    0x02: 'Ethernet Indicator',
    0x03: 'WiFi Indicator',
    0x04: 'Software Indicator',
    0x05: 'Power Limit Indicator',
    0x06: 'Disable'
}

LED_TYPE = {
    'legacy': {
        0x01: 'S0 Power LED',
        0x02: 'S0 Ring LED'
    },
    'new': {
        0x00: 'Power Button LED',
        0x01: 'HDD LED',
        0x02: 'Skull LED',
        0x03: 'Eyes LED',
        0x04: 'Front LED1',
        0x05: 'Front LED2',
        0x06: 'Front LED3',
    }
}

CONTROL_ITEM_ETHERNET_INDICATOR_TYPE = {
    0x00: 'LAN1',
    0x01: 'LAN2',
    0x02: 'LAN1 + LAN2'
}

CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'Type',
        'Options': CONTROL_ITEM_ETHERNET_INDICATOR_TYPE
    },
    0x01: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x02: {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    0x03: {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x04: {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    }
}

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR = {
    0x00: 'Normally OFF, ON when active',
    0x01: 'Normally ON, OFF when active'
}

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x01: {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    0x02: {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x03: {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x04: {
        'Control Item': 'Behavior',
        'Options': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR
    }
}

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_SINGLE_COLOR = {
    0x00: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    0x01: {
        'Control Item': 'Behavior',
        'Options': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR
    }
}

CONTROL_ITEM_POWER_LIMIT_INDICATOR_INDICATION_SCHEME = {
    0x00: 'Green to Red',
    0x01: 'Single Color'
}

CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'Indication Scheme',
        'Options': CONTROL_ITEM_POWER_LIMIT_INDICATOR_INDICATION_SCHEME
    },
    0x01: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x02: {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    0x03: {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x04: {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    }
}

CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'S0 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x01: {
        'Control Item': 'S0 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    0x02: {
        'Control Item': 'S0 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREEQUENCY['new']
    },
    0x03: {
        'Control Item': 'S0 Indicator Color',
        'Options': LED_COLOR['new']
    },
    0x04: {
        'Control Item': 'S0 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x05: {
        'Control Item': 'S0 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x06: {
        'Control Item': 'S3 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x07: {
        'Control Item': 'S3 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    0x08: {
        'Control Item': 'S3 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREEQUENCY['new']
    },
    0x09: {
        'Control Item': 'S3 Indicator Color',
        'Options': LED_COLOR['new']
    },
    0x0A: {
        'Control Item': 'S3 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x0B: {
        'Control Item': 'S3 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x0C: {
        'Control Item': 'Modern Standby Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x0D: {
        'Control Item': 'Modern Standby Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    0x0E: {
        'Control Item': 'Modern Standby Indicator Blinking Frequency',
        'Options': LED_BLINK_FREEQUENCY['new']
    },
    0x0F: {
        'Control Item': 'Modern Standby Indicator Color',
        'Options': LED_COLOR['new']
    },
    0x10: {
        'Control Item': 'Modern Standby Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x11: {
        'Control Item': 'Modern Standby Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x12: {
        'Control Item': 'S5 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x13: {
        'Control Item': 'S5 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    0x14: {
        'Control Item': 'S5 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREEQUENCY['new']
    },
    0x15: {
        'Control Item': 'S5 Indicator Color',
        'Options': LED_COLOR['new']
    },
    0x16: {
        'Control Item': 'S5 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x17: {
        'Control Item': 'S5 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    },
}

CONTROL_ITEM_POWER_STATE_INDICATOR_SINGLE_COLOR = {
    0x00: {
        'Control Item': 'S0 Indicator Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    0x01: {
        'Control Item': 'S0 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    },
    0x02: {
        'Control Item': 'S3 Indicator Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    0x03: {
        'Control Item': 'S3 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    }
}

CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x01: {
        'Control Item': 'Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    0x02: {
        'Control Item': 'Blinking Frequency',
        'Options': LED_BLINK_FREEQUENCY['new']
    },
    0x03: {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    0x04: {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x05: {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    }
}

CONTROL_ITEM_SOFTWARE_INDICATOR_SINGLE_COLOR = {
    0x00: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    0x01: {
        'Control Item': 'Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    }
}

CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR = {
    0x00: {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    0x01: {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    0x02: {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']
    },
    0x03: {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']
    }
}

CONTROL_ITEM = {
    # LED Indicator Option

    # Power State Indicator
    0x00: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: CONTROL_ITEM_POWER_STATE_INDICATOR_SINGLE_COLOR
    },

    # HDD Activity Indicator
    0x01: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_SINGLE_COLOR
    },

    # Ethernet Indicator
    0x02: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: None
    },

    # Wifi Indicator
    0x03: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: None
    },

    # Software Indicator
    0x04: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: CONTROL_ITEM_SOFTWARE_INDICATOR_SINGLE_COLOR
    },

    # Power Limit Indicator
    0x05: {
        # LED color type

        # Dual-color Blue / Amber
        0x00: CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        0x01: CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # RGB-color
        0x02: CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # Single-color LED
        0x03: None
    },

    # Disable
    0x06: None
}

# Return value of FF FF FF FF is specific to the driver, not the actual WMI implementation.
# Some of these return errors are the generic NUC WMI errors, not all are specific to the NUC LEDs.
RETURN_ERROR = {
    0xE1: 'Error (Function not supported)',
    0xE2: 'Error (Undefined device)',
    0xE3: 'Error (EC doesn\'t respond)',
    0xE4: 'Error (Invalid Parameter)',
    0xE5: 'Error (Node busy. Command could not be executed because ' +
    'command processing resources are temporarily unavailable.)',
    0xE6: 'Error (Command execution failure. ' +
    'Parameter is illegal because destination device has been disabled or is unavailable)',
    0xE7: 'Error (Invalid CEC Opcode)',
    0xE8: 'Error (Data Buffer size is not enough)',
    0xEF: 'Error (Unexpected error)',
    0xFF: 'Error (Return value has already been read and reset)'
}

class NucWmiError(Exception):
    pass
