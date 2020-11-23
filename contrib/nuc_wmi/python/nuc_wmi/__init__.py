"""
nuc_wmi CLI userland for the Intel NUC LED kernel module.
"""

CONTROL_FILE = '/proc/acpi/nuc_led'

LED_BLINK_BEHAVIOR_MULTI_COLOR = [
    'Solid',
    'Breathing',
    'Pulsing',
    'Strobing'
]

LED_BLINK_BEHAVIOR_SINGLE_COLOR = [
    '1Hz',
    '0.25Hz',
    '1Hz Fade',
    '0.25Hz Fade',
    'Always On'
]

LED_BLINK_BEHAVIOR = [
    # Index = LED Color Type

    # Dual-color Blue / Amber
    LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # Dual-color Blue / White
    LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # RGB-color
    LED_BLINK_BEHAVIOR_MULTI_COLOR,

    # Single-color LED
    LED_BLINK_BEHAVIOR_SINGLE_COLOR
]

LED_BLINK_FREQUENCY = {
    # NUC 7:
    #   - Using BIOS AY0029 or BN0042, only 0x01-0x04 are available.
    #   - Using BIOS AY0038 or BN0043, all frequencies are available.
    'legacy': [
        None,
        '1Hz',
        '0.25Hz',
        '1Hz fade',
        'Always on',
        '0.5Hz',
        '0.25Hz fade',
        '0.5Hz fade'
    ],
    'new': [
        None,
        '0.1Hz',
        '0.2Hz',
        '0.3Hz',
        '0.4Hz',
        '0.5Hz',
        '0.6Hz',
        '0.7Hz',
        '0.8Hz',
        '0.9Hz',
        '1.0Hz'
    ]
}

LED_BRIGHTNESS_MULTI_COLOR = [str(brightness) for brightness in range(0x00, 0x64 + 1)]

LED_BRIGHTNESS_SINGLE_COLOR = [
    'OFF',
    '50%',
    '100%'
]

LED_BRIGHTNESS = {
    'legacy': LED_BRIGHTNESS_MULTI_COLOR,
    'new': [
        # Index = LED color type

        # Dual-color Blue / Amber
        LED_BRIGHTNESS_MULTI_COLOR,

        # Dual-color Blue / White
        LED_BRIGHTNESS_MULTI_COLOR,

        # RGB-color
        LED_BRIGHTNESS_MULTI_COLOR,

        # Single-color LED
        LED_BRIGHTNESS_SINGLE_COLOR
    ]
}

LED_COLOR = {
    'legacy': {
        'Dual-color Blue / Amber': [
            'Disable',
            'Blue',
            'Amber'
        ],
        'RGB-color': [
            'Disable',
            'Cyan',
            'Pink',
            'Yellow',
            'Blue',
            'Red',
            'Green',
            'White'
        ]
    },
    'new': {
        'Dual-color Blue / Amber': [
            'Blue',
            'Amber'
        ],
        'Dual-color Blue / White': [
            'Blue',
            'White'
        ],
        'RGB-color': {
            '1d':  {
                'HDD LED': [
                    None,
                    'Blue',
                    'Red',
                    'Green',
                    'Orange',
                    'Yellow',
                    'Indigo',
                    'Violet',
                    'White'
                ],
                'RGB Header': [
                    None,
                    'Cyan',
                    'Magenta',
                    'Yellow',
                    'Blue',
                    'Red',
                    'Green',
                    'White'
                ]
            },
            '3d': [str(rgb) for rgb in range(0x00, 0xFF + 1)]
        }
    }
}

LED_COLOR_TYPE = {
    'legacy': {
        'S0 Power LED': 'Dual-color Blue / Amber',
        'S0 Ring LED': 'RGB-color'
    },
    'new': [
        'Dual-color Blue / Amber',
        'Dual-color Blue / White',
        'RGB-color',
        'Single-color LED'
    ]
}

LED_INDICATOR_OPTION = [
    'Power State Indicator',
    'HDD Activity Indicator',
    'Ethernet Indicator',
    'WiFi Indicator',
    'Software Indicator',
    'Power Limit Indicator',
    'Disable'
]

LED_TYPE = {
    'legacy': [
        None,
        'S0 Power LED',
        'S0 Ring LED'
    ],
    'new': [
        'Power Button LED',
        'HDD LED',
        'Skull LED',
        'Eyes LED',
        'Front LED1',
        'Front LED2',
        'Front LED3',
        'RGB Header'
    ]
}

CONTROL_ITEM_ETHERNET_INDICATOR_TYPE = [
    'LAN1',
    'LAN2',
    'LAN1 + LAN2'
]

CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'Type',
        'Options': CONTROL_ITEM_ETHERNET_INDICATOR_TYPE
    },
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    }
]

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR = [
    'Normally OFF, ON when active',
    'Normally ON, OFF when active'
]

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Behavior',
        'Options': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR
    }
]

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_SINGLE_COLOR = [
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    {
        'Control Item': 'Behavior',
        'Options': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR
    }
]

CONTROL_ITEM_POWER_LIMIT_INDICATOR_INDICATION_SCHEME = [
    'Green to Red',
    'Single Color'
]

CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'Indication Scheme',
        'Options': CONTROL_ITEM_POWER_LIMIT_INDICATOR_INDICATION_SCHEME
    },
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    }
]

CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'S0 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'S0 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    {
        'Control Item': 'S0 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREQUENCY['new']
    },
    {
        'Control Item': 'S0 Indicator Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'S0 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'S0 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'S3 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'S3 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    {
        'Control Item': 'S3 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREQUENCY['new']
    },
    {
        'Control Item': 'S3 Indicator Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'S3 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'S3 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Modern Standby Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Modern Standby Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    {
        'Control Item': 'Modern Standby Indicator Blinking Frequency',
        'Options': LED_BLINK_FREQUENCY['new']
    },
    {
        'Control Item': 'Modern Standby Indicator Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Modern Standby Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Modern Standby Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'S5 Indicator Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'S5 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    {
        'Control Item': 'S5 Indicator Blinking Frequency',
        'Options': LED_BLINK_FREQUENCY['new']
    },
    {
        'Control Item': 'S5 Indicator Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'S5 Indicator Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'S5 Indicator Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    }
]

CONTROL_ITEM_POWER_STATE_INDICATOR_SINGLE_COLOR = [
    {
        'Control Item': 'S0 Indicator Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    {
        'Control Item': 'S0 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    },
    {
        'Control Item': 'S3 Indicator Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    {
        'Control Item': 'S3 Indicator Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    }
]

CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_MULTI_COLOR
    },
    {
        'Control Item': 'Blinking Frequency',
        'Options': LED_BLINK_FREQUENCY['new']
    },
    {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    }
]

CONTROL_ITEM_SOFTWARE_INDICATOR_SINGLE_COLOR = [
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_SINGLE_COLOR
    },
    {
        'Control Item': 'Blinking Behavior',
        'Options': LED_BLINK_BEHAVIOR_SINGLE_COLOR
    }
]

CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR = [
    {
        'Control Item': 'Brightness',
        'Options': LED_BRIGHTNESS_MULTI_COLOR
    },
    {
        'Control Item': 'Color',
        'Options': LED_COLOR['new']
    },
    {
        'Control Item': 'Color 2',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    },
    {
        'Control Item': 'Color 3',
        'Options': LED_COLOR['new']['RGB-color']['3d']
    }
]

CONTROL_ITEM = [
    # Index = LED Indicator Option

    # Power State Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_POWER_STATE_INDICATOR_MULTI_COLOR,

        # Single-color LED
        CONTROL_ITEM_POWER_STATE_INDICATOR_SINGLE_COLOR
    ],

    # HDD Activity Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR,

        # Single-color LED
        CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_SINGLE_COLOR
    ],

    # Ethernet Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_ETHERNET_INDICATOR_MULTI_COLOR,

        # Single-color LED
        None
    ],

    # Wifi Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_WIFI_INDICATOR_MULTI_COLOR,

        # Single-color LED
        None
    ],

    # Software Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR,

        # Single-color LED
        CONTROL_ITEM_SOFTWARE_INDICATOR_SINGLE_COLOR
    ],

    # Power Limit Indicator
    [
        # Index = LED color type

        # Dual-color Blue / Amber
        CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # Dual-color Blue / White
        CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # RGB-color
        CONTROL_ITEM_POWER_LIMIT_INDICATOR_MULTI_COLOR,

        # Single-color LED
        None
    ],

    # Disable
    None
]

QUIRKS_AVAILABLE = [
    'NUC7_FREQUENCY_DEFAULT',
    'NUC10_RETURN_VALUE'
]

# Return value of FF FF FF FF is specific to the driver, not the actual WMI implementation.
# Some of these return errors are the generic NUC WMI errors, not all are specific to the NUC LEDs.
RETURN_ERROR = {
    0xE1: 'Error (Function not supported)',
    0xE2: 'Error (Undefined device)',
    0xE3: 'Error (EC doesn\'t respond)',
    0xE4: 'Error (Invalid Parameter)',
    0xE5: 'Error (Node busy. Command could not be executed because ' + \
    'command processing resources are temporarily unavailable.)',
    0xE6: 'Error (Command execution failure. ' + \
    'Parameter is illegal because destination device has been disabled or is unavailable)',
    0xE7: 'Error (Invalid CEC Opcode)',
    0xE8: 'Error (Data Buffer size is not enough)',
    0xEF: 'Error (Unexpected error)',
    0xFF: 'Error (Return value has already been read and reset)'
}

class NucWmiError(Exception):
    """
    NUC WMI error exception type.
    """
    pass # pylint: disable=unnecessary-pass
