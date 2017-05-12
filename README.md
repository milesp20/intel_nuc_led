This is a simple kernel module to control the power and ring LEDs on Intel NUC7i[x]BN and NUC6CAY kits.

This module is intended as a demonstration/proof-of-concept and may not be maintained further.  Perhaps
it can act as a jumping off point for a more polished and complete implementation.  For testing and basic
manipulation of the power LED and ring LED, it ought to work fine, but use with caution none the less.

Requirements:

* Intel NUC7i[x]BN and NUC6CAY
* BIOS AY0038 or BN0043 or later
* ACPI/WMI support in kernel
* LED(s) set to SW Control in BIOS
    
This driver works via '/proc/acpi/nuc_led'.  To get current LED state:

    cat /proc/acpi/nuc_led
    
To change the LED state:

    echo '<led>,<brightness>,<blink/fade>,<color>' | sudo tee /proc/acpi/nuc_led > /dev/null
    
LEDs:

* power - the power button LED
* ring  - the ring LED surrounding the front panel
    
Brightness:

* any integer between 0 and 100

Blink/fade:

* none          solid/always on
* blink_slow    0.25Hz blink
* blink_medium  0.5Hz blink
* blink_fast    1Hz blink
* fade_slow     0.25Hz blink
* fade_medium   0.5Hz blink
* fade_fast     1Hz blink
    
Color (power LED):

* off
* blue
* amber
    
Color (ring LED):

* off
* cyan
* pink
* yellow
* blue
* red
* green
* white
    
Example execution to cause the ring LED blink green at a medium rate at partial intensity:

    echo 'ring,80,blink_medium,green' | sudo tee /proc/acpi/nuc_led > /dev/null
    
Errors in passing parameters will appear as warnings in dmesg.
