# NUC WMI Function regression test plan

The tests should be run in the order specified here. The tests include argument values that span the beginning
and end of the enum range for each input value type to ensure we no longer have any more issues with processing
of the WMI return values.

Note: When running HDD Activity tests, you can use
`dd if=/dev/random of=/tmp/empty_raw_file bs=1M count=1000 status=progress; rm -f /tmp/empty_raw_file`
to trigger blinking from writing on SSDs.

## nuc_wmi-get_led

### NUC 7

```
$ nuc_wmi-get_led 'NUC_7' 'S0 Power LED'
{"error": "Error (Undefined device)"}

$ nuc_wmi-get_led 'NUC_7' 'S0 Ring LED'
{"led": {"color": "White", "frequency": "Always on", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}
```

If software control is not enabled in BIOS, commands return `{"error": "Error (Undefined device)"}` error.

### NUC 10 (BIOS older than Dec 2020)

N/A

### NUC 10 (BIOS Dec 2020 or newer)

N/A

### NUC 12 (initial release BIOS)

N/A

----

## nuc_wmi-set_led

### NUC 7

```
$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 0 '1Hz' 'Disable'
{"led": {"color": "Disable", "frequency": "1Hz", "type": "S0 Ring LED", "brightness": "0"}, "nuc_wmi_spec_alias": "NUC_7"}

$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 100 '1Hz' 'Disable'
{"led": {"color": "Disable", "frequency": "1Hz", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}

$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 0 '1Hz' 'Cyan'
{"led": {"color": "Cyan", "frequency": "1Hz", "type": "S0 Ring LED", "brightness": "0"}, "nuc_wmi_spec_alias": "NUC_7"}

$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 100 '1Hz' 'Cyan'
{"led": {"color": "Cyan", "frequency": "1Hz", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}

$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 100 '0.5Hz fade' 'White'
{"led": {"color": "White", "frequency": "0.5Hz fade", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}

$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 100 '0.5Hz fade' 'Green'
{"led": {"color": "Green", "frequency": "0.5Hz fade", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}
```

### NUC 10 (BIOS older than Dec 2020)

N/A

### NUC 10 (BIOS Dec 2020 or newer)

N/A

### NUC 12 (initial release BIOS)

N/A

---

## nuc_wmi-query_leds

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-query_leds 'NUC_10_OLD_BIOS'
{"leds": ["Power Button LED", "HDD LED"], "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-query_leds 'NUC_10'
{"leds": ["Power Button LED", "HDD LED", "RGB Header"], "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-query_leds 'NUC_12'
{"leds": ["Power Button LED"], "nuc_wmi_spec_alias": "NUC_12", "nuc_wmi_spec_alias": "NUC_12"}
```

---

## nuc_wmi-query_led_color_type

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-query_led_color_type 'NUC_10_OLD_BIOS' 'Power Button LED'
{"led": {"color_type": "Dual-color Blue / Amber", "type": "Power Button LED"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-query_led_color_type 'NUC_10_OLD_BIOS' 'HDD LED'
{"led": {"color_type": "Dual-color Blue / White", "type": "HDD LED"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-query_led_color_type 'NUC_10' 'Power Button LED'
{"led": {"color_type": "Dual-color Blue / Amber", "type": "Power Button LED"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_color_type 'NUC_10' 'HDD LED'
{"led": {"color_type": "RGB-color", "type": "HDD LED"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_color_type 'NUC_10' 'RGB Header'
{"led": {"color_type": "RGB-color", "type": "RGB Header"}, "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-query_led_color_type 'NUC_12' 'Power Button LED'
{"led": {"color_type": "RGB-color", "type": "Power Button LED"}, "nuc_wmi_spec_alias": "NUC_12"}
```

---

## nuc_wmi-query_led_indicator_options

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-query_led_indicator_options 'NUC_10_OLD_BIOS' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-query_led_indicator_options 'NUC_10_OLD_BIOS' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_options": ["HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-query_led_indicator_options 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_indicator_options 'NUC_10' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_options": ["HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_indicator_options 'NUC_10' 'RGB Header'
{"led": {"type": "RGB Header", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-query_led_indicator_options 'NUC_12' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_12"}
```

---

## nuc_wmi-query_led_control_items

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-query_led_control_items 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator'
{"led": {"control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color"], "type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-query_led_control_items 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Color 2", "Color 3"], "type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-query_led_control_items 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-query_led_control_items 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Behavior"], "type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-query_led_control_items 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-query_led_control_items 'NUC_10' 'Power Button LED' 'Power State Indicator'
{"led": {"control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color", "S3 Indicator Brightness", "S3 Indicator Blinking Behavior", "S3 Indicator Blinking Frequency", "S3 Indicator Color"], "type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Behavior"], "type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'Power Button LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-query_led_control_items 'NUC_10' 'HDD LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Behavior"], "type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'HDD LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-query_led_control_items 'NUC_10' 'RGB Header' 'Power State Indicator'
{"led": {"control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color", "S3 Indicator Brightness", "S3 Indicator Blinking Behavior", "S3 Indicator Blinking Frequency", "S3 Indicator Color"], "type": "RGB Header", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'RGB Header' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Behavior"], "type": "RGB Header", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'RGB Header' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "RGB Header", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-query_led_control_items 'NUC_12' 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator", "control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color", "S0 Indicator Color 2", "S0 Indicator Color 3", "Modern Standby Indicator Brightness", "Modern Standby Indicator Blinking Behavior", "Modern Standby Indicator Blinking Frequency", "Modern Standby Indicator Color", "Modern Standby Indicator Color 2", "Modern Standby Indicator Color 3"]}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-query_led_control_items 'NUC_12' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_items": ["Brightness", "Color", "Color 2", "Color 3", "Behavior"]}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-query_led_control_items 'NUC_12' 'Power Button LED' 'Software Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color", "Color 2", "Color 3"]}, "nuc_wmi_spec_alias": "NUC_12"}
```

---

## nuc_wmi-get_led_control_item, nuc_wmi-set_led_control_item, nuc_wmi-get_led_indicator_option, nuc_wmi-set_led_indicator_option

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-set_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness' 100
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Solid
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '1.0Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Blue
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Strobing
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '0.1Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Amber
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Color' Amber
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_indicator_option 'NUC_10_OLD_BIOS' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Color' Amber
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_indicator_option 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator'
{"led": {"type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_indicator_option 'NUC_10_OLD_BIOS' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color' Yellow
{"error": "Invalid control item value for the specified control item"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_indicator_option 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_indicator_option 'NUC_10_OLD_BIOS' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}


$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}

$ nuc_wmi-set_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color' Yellow
{"error": "Invalid control item value for the specified control item"}

$ nuc_wmi-get_led_control_item 'NUC_10_OLD_BIOS' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-set_led_indicator_option 'NUC_10' 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness' 100
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Solid
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '1.0Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Blue
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Strobing
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '0.1Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Amber
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Color' Amber
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'Power Button LED' 'Software Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Color' Amber
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Amber"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'HDD LED' 'HDD Activity Indicator'
{"led": {"type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color' Yellow
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'HDD LED' 'Software Indicator'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color' Yellow
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'RGB Header' 'Power State Indicator'
{"led": {"type": "RGB Header", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'RGB Header'
{"led": {"type": "RGB Header", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Brightness' 100
{"led": {"control_item": "S0 Indicator Brightness", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Solid
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '1.0Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color' Blue
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Strobing
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '0.1Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color' White
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color' Green
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Green"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "RGB Header", "indicator_option": "Power State Indicator", "control_item_value": "Green"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'RGB Header' 'HDD Activity Indicator'
{"led": {"type": "RGB Header", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'RGB Header'
{"led": {"type": "RGB Header", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color' Yellow
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "HDD Activity Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_indicator_option 'NUC_10' 'RGB Header' 'Software Indicator'
{"led": {"type": "RGB Header", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'RGB Header'
{"led": {"type": "RGB Header", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}


$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color' Blue
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color' White
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color' Yellow
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_control_item 'NUC_10' 'RGB Header' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "RGB Header", "indicator_option": "Software Indicator", "control_item_value": "Yellow"}, "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-set_led_indicator_option 'NUC_12' 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_indicator_option 'NUC_12' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}


$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness' 100
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Solid
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '1.0Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' 0
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 2' 0
{"led": {"control_item": "S0 Indicator Color 2", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 3' 100
{"led": {"control_item": "S0 Indicator Color 3", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 2'
{"led": {"control_item": "S0 Indicator Color 2", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 3'
{"led": {"control_item": "S0 Indicator Color 3", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior' Strobing
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency' '0.1Hz'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' 255
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 2' 191
{"led": {"control_item": "S0 Indicator Color 2", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 3' 0
{"led": {"control_item": "S0 Indicator Color 3", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Behavior'
{"led": {"control_item": "S0 Indicator Blinking Behavior", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Blinking Frequency'
{"led": {"control_item": "S0 Indicator Blinking Frequency", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 2'
{"led": {"control_item": "S0 Indicator Color 2", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color 3'
{"led": {"control_item": "S0 Indicator Color 3", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}


$ nuc_wmi-set_led_indicator_option 'NUC_12' 'Power Button LED' 'HDD Activity Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_indicator_option 'NUC_12' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}


$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color' 0
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 2' 0
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 3' 100
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally OFF, ON when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 2'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 3'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally OFF, ON when active"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Behavior' 'Normally ON, OFF when active'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color' 255
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 2' 192
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 3' 0
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Behavior'
{"led": {"control_item": "Behavior", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "Normally ON, OFF when active"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 2'
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'HDD Activity Indicator' 'Color 3'
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "HDD Activity Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}


$ nuc_wmi-set_led_indicator_option 'NUC_12' 'Power Button LED' 'Software Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_indicator_option 'NUC_12' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_12"}


$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Solid
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color' 0
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 2' 0
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 3' 100
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Solid"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Blue
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 2'
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 3'
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Behavior' Strobing
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Frequency' '0.1Hz'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color' 255
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 2' 191
{"led": {"control_item": "Color 2", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-set_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 3' 0
{"led": {"control_item": "Color 3", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Behavior'
{"led": {"control_item": "Blinking Behavior", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "Strobing"}, "nuc_wmi_spec_alias": "NUC_12"}

$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0.1Hz"}, "nuc_wmi_spec_alias": "NUC_12"}

# Amber
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 2'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "191"}, "nuc_wmi_spec_alias": "NUC_12"}
$ nuc_wmi-get_led_control_item 'NUC_12' 'Power Button LED' 'Software Indicator' 'Color 3'
{"led": {"control_item": "Color", "type": "Power Button LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_12"}
```

Note: NUC 12 power button LED is a 3D RGB LED that uses PWM and not a 1D LED that uses color labels.

---

## nuc_wmi-save_led_config

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-save_led_config 'NUC_10_OLD_BIOS'
{"led_app_notification": {"type": "save_led_config"}, "nuc_wmi_spec_alias": "NUC_10_OLD_BIOS"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-save_led_config 'NUC_10'
{"led_app_notification": {"type": "save_led_config"}, "nuc_wmi_spec_alias": "NUC_10"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-save_led_config 'NUC_12'
{"led_app_notification": {"type": "save_led_config"}, "nuc_wmi_spec_alias": "NUC_12"}
```

Rebooting/hard power off should cause the device to resume with the last configued LED states.

---

## nuc_wmi-switch_led_type

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-switch_led_type 'NUC_10_OLD_BIOS' 'Single color LED'
{"error": "Error (Function not supported)"}

$ nuc_wmi-switch_led_type 'NUC_10_OLD_BIOS' 'Multi color LED'
{"error": "Error (Function not supported)"}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-switch_led_type 'NUC_10' 'Single color LED'
{"error": "Error (Function not supported)"}

$ nuc_wmi-switch_led_type 'NUC_10' 'Multi color LED'
{"error": "Error (Function not supported)"}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-switch_led_type 'NUC_12' 'Single color LED'

$ nuc_wmi-switch_led_type 'NUC_12' 'Multi color LED'
```

This WMI function doesnt work on NUC 10. I dont know what its for.

---

## nuc_wmi-wmi_interface_spec_compliance_version

### NUC 7

N/A

### NUC 10 (BIOS older than Dec 2020)

```
$ nuc_wmi-wmi_interface_spec_compliance_version 'NUC_10_OLD_BIOS'
{"nuc_wmi_spec_alias": "NUC_10_OLD_BIOS", "version": {"semver": "1.32", "type": "wmi_interface_spec_compliance"}}
```

### NUC 10 (BIOS Dec 2020 or newer)

```
$ nuc_wmi-wmi_interface_spec_compliance_version 'NUC_10'
{"nuc_wmi_spec_alias": "NUC_10", "version": {"semver": "1.32", "type": "wmi_interface_spec_compliance"}}
```

### NUC 12 (initial release BIOS)

```
$ nuc_wmi-wmi_interface_spec_compliance_version 'NUC_12'
{"nuc_wmi_spec_alias": "NUC_12", "version": {"semver": "1.40", "type": "wmi_interface_spec_compliance"}}
```
