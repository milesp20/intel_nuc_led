# Intel NUC7i[x]BN and NUC6CAY LED Control

This is a simple kernel module to control the power and ring LEDs on Intel NUC7i[x]BN and NUC6CAY kits.

This module is intended as a demonstration/proof-of-concept and may not be maintained further.  Perhaps
it can act as a jumping off point for a more polished and complete implementation.  For testing and basic
manipulation of the power LED and ring LED, it ought to work fine, but use with caution none the less. This
has only been tested on 4.4.x kernels.


## Requirements

Requirements:

* Intel NUC7i[x]BN and NUC6CAY
* BIOS AY0038 or BN0043 or later
* ACPI/WMI support in kernel
* LED(s) set to `SW Control` in BIOS

## Building

THe `nuc_led` kernel module supports building and installing "from source" directly or using `dkms`.

### Installing Build Dependencies

Ubuntu:

```
apt-get install build-essential linux-headers-$(uname -r)

# DKMS dependencies
apt-get install debhelper dkms
```

Redhat:

```
yum groupinstall "Development Tools"
yum install kernel-devel-$(uname -r)

# Install appropriate EPEL for DKMS if needed by your RHEL variant
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

yum install dkms
```

### Building and Installing "from source"

```
make clean
make install
```

### Building and Installing Using DKMS

Build and install without system packaging:

```
make dkms-install
```

Uninstall without system packaging:

```
make dkms-uninstall
```

Build and install using system packaging:

```
# Ubuntu
make dkms-deb

# RHEL
make dkms-rpm

# Install generated DEB/RPM from the folder specified in the output using system package manager
```

## Usage
    
This driver works via '/proc/acpi/nuc_led'.  To get current LED state:

```
cat /proc/acpi/nuc_led
```
    
To change the LED state:

```
 echo '<led>,<brightness>,<blink/fade>,<color>' | sudo tee /proc/acpi/nuc_led > /dev/null
```

|LED  |Description                              |
|-----|-----------------------------------------|
|power|The power button LED.                    |
|ring |The ring LED surrounding the front panel.|

Brightness:

* any integer between `0` and `100`.

|Blink/Fade Option|Description    |
|-----------------|---------------|
|blink\_fast      |1Hz blink      |
|blink\_medium    |0.5Hz blink    |
|blink\_slow      |0.25Hz blink   |
|fade\_fast       |1Hz blink      |
|fade\_medium     |0.5Hz blink    |
|fade\_slow       |0.25Hz blink   |
|none             |solid/always on|

|LED Color|power|ring|
|---------|:---:|:--:|
|amber    |X    |    |
|cyan     |     |X   |
|blue     |X    |X   |
|green    |     |X   |
|off      |X    |X   |
|pink     |     |X   |
|red      |     |X   |
|white    |     |X   |
|yellow   |     |X   |
    
Example execution to cause the ring LED blink green at a medium rate at partial intensity:

    echo 'ring,80,blink_medium,green' | sudo tee /proc/acpi/nuc_led > /dev/null
    
Errors in passing parameters will appear as warnings in dmesg.

You can change the owner, group and permissions of `/proc/acpi/nuc_led` by passing parameters to the nuc_led kernel module. Use:

* `nuc_led_uid` to set the owner (default is 0, root)
* `nuc_led_gid` to set the owning group (default is 0, root)
* `nuc_led_perms` to set the file permissions (default is r+w for group and user and r for others)

Note: Once an LED has been set to `SW Control` in the BIOS, it will remain off initially until a color is explicitly set, after which the set color is retained across reboots.
