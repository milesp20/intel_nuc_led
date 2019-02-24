# Intel NUC7i[x]BN and NUC6CAY LED Control

This is a simple kernel module to control the power and ring LEDs on Intel NUC7i[x]BN and NUC6CAY/H kits.

This module is intended as a polished and complete implementation for basic manipulation of 
the power LED and ring LED.  This has only been tested on 4.4.x and 4.15.x kernels.


<hr>

## 1) Requirements

* Intel NUC7i[x]BN and NUC6CA[x]
* BIOS AY0038 or BN0043 or later
* ACPI/WMI support in kernel
* LED(s) set to `SW Control` in BIOS

<hr>

## 2) Usage

This driver works via '/proc/acpi/nuc_led'.  To get current LED state:

```
cat /proc/acpi/nuc_led
```

To change the LED state:

```
 echo '<led>,<brightness>,<blink/fade>,<color>' | sudo tee /proc/acpi/nuc_led > /dev/null
```

To change the LED state profile:

```
 echo '<led>,<brightness>,<blink/fade>,<color>,<profile>' | sudo tee /proc/acpi/nuc_led > /dev/null
```

To view a specific LED state profile:

```
 echo 'view,<profile>' | sudo tee /proc/acpi/nuc_led > /dev/null
 cat /proc/acpi/nuc_led
```

To set a specific LED state profile:

```
 echo 'profile,<profile>' | sudo tee /proc/acpi/nuc_led > /dev/null
```

<hr>

## 3) Parameters

#### First Parameter:

|LED    |Number|Description                              |
|-------|------|-----------------------------------------|
|power  |1     |The power button LED.                    |
|ring   |2     |The ring LED surrounding the front panel.|
|profile|      |Set a specific profile (next parameter)  |
|view   |      |View a specific profile (next parameter) |

#### Second Parameter:

|Brightness|Number  |Description     |
|----------|:------:|----------------|
|0 to 100  |0 to 100|Brightness value|
|current   |-1      |Current Setting |


#### Third Parameter:


|Blink/Fade Option|Number|Description    |What It Means                |
|-----------------|:----:|---------------|-----------------------------|
|blink\_fast      |1     |1Hz Blink      |1 Blink per second           |
|blink\_medium    |5     |0.5Hz Blink    |1 Blink every 2 seconds      |
|blink\_slow      |2     |0.25Hz Blink   |1 Blink every 4 seconds      |
|fade\_fast       |3     |1Hz Fade       |1 Fade In/Out every 1 second |
|fade\_medium     |7     |0.5Hz Fade     |1 Fade In/Out every 2 seconds|
|fade\_slow       |6     |0.25Hz Fade    |1 Fade In/Out every 4 seconds|
|none             |4     |Solid/Always on|Solid/Always on              |
|solid            |4     |Solid/Always on|Solid/Always on              |
|off              |4     |Solid/Always on|Solid/Always on              |
|current          |-1    |Current Setting|Current Setting              |

#### Fourth Parameter:

|Power LED Colors|Number|
|----------------|:----:|
|amber           |2     |
|blue            |1     |
|off             |0     |
|current         |-1    |

|Ring LED Colors|Number|
|---------------|:----:|
|cyan           |1     |
|blue           |4     |
|green          |6     |
|off            |0     |
|pink           |2     |
|red            |5     |
|white          |7     |
|yellow         |3     |
|current        |-1    |

#### Profile Names (Optional):

|Profile Names|Number|When Automatically Used       |
|-------------|:----:|------------------------------|
|current      |0     |Current settings              |
|boot         |1     |At boot                       |
|shutdown     |2     |At shutdown                   |
|suspend      |3     |When entering S3 standby      |
|wake         |4     |When exiting S3 standby       |
|hibernate    |5     |When entering hibernation mode|
|restore      |6     |When exiting hibernation mode |
|recording    |7     |                              |
|voice        |8     |                              |

<hr>

## 4) Examples

1) Ring LED blinks green at a medium rate at partial intensity:

```
echo 'ring,80,blink_medium,green' | sudo tee /proc/acpi/nuc_led > /dev/null
```

2) Ring LED blinks green at a medium rate at partial intensity, using only numbers:

```
echo '2,80,5,6' | sudo tee /proc/acpi/nuc_led > /dev/null
```

3) Ring LED blinks green at a medium rate at partial intensity at boot:

```
echo 'ring,80,blink_medium,green,boot' | sudo tee /proc/acpi/nuc_led > /dev/null
```

4) Ring LED blinks green at a medium rate at partial intensity at boot, using only numbers:

```
echo '2,80,5,6,1' | sudo tee /proc/acpi/nuc_led > /dev/null
```

Errors in passing parameters will appear as warnings in dmesg.

<hr>

## 5) Module Parameters

You can change the owner, group and permissions of `/proc/acpi/nuc_led`, enable a more detailed
debugging mode, hibernate/suspend mode treatment, as well as pass the profiles you want the module 
to use by passing parameters to the nuc_led kernel module. Use:

* `nuc_led_uid` to set the owner (default is 0, root)
* `nuc_led_gid` to set the owning group (default is 0, root)
* `nuc_led_perms` to set the file permissions (default is r+w for group and user and r for others)
* `nuc_led_profiles` to set the profile settings desired (defaults to current settings for all profiles, see under #7)
* `debug` to set to non-zero value for more detailed debugging (default is 0, off)
* `hibernate_same` to non-zero to treat hibernation events as `suspend` and `wake` events.  (default is 1, on)

<hr>

## 6) Setting Parameters After Module Is Loaded

Once the module is loaded, you can change three parameters.  They are:

1) `/sys/module/nuc_led/parameters/debug` can be both read and written to.  By writing, you can 
set to either a non-zero value or zero in order to change the debugging state.

2) `/sys/module/nuc_led/parameters/nuc_led_profiles` can be both read and written to.  By writing, 
you can set all profiles at the same time.  By reading, you can get all of the profile settings 
as a semicolon-seperated string.  See notes under #7.

3) `/sys/module/nuc_led/parameters/hibernate_same` can be both read and written to.  By writing, you 
can set a non-zero value to treat hibernation events as `suspend` and `wake` events.

<hr>

## 7) Notes About Profiles

By default, all profiles are equal to "current brightness, blink/fade and color settings".  Using the 
module parameters allows the module installer (generally root) to specify what settings should be 
used at during each stage of the computer's usage.

Profile `current` specifies the current settings of the LED lights.  This is always implied when a
profile name (or profile ID) is not specified.  If a request is written to the module to read a 
particular profile, the very next read will return the "current" profile, instead of returning the
specified profile again.

Profile `boot` is always invoked during the module startup and is intended to indicate that the
computer has "booted".  Note that reloading the module will invoke the `boot` profile, however, I
am not sure if `modprobe` pulls the parameters from the module configuration file at that time.  I
know it does at boot time...

If the `hibernate_same` flag is set to a non-zero value, then the following happens:

1) `hibernate` mode is treated as a `suspend` mode by the module
2) `restore` is treated as a `wake` mode by the module
3) `hibernate` and `restore` profiles are NEVER used/called!

Profile `shutdown` is always invoked during the shutdown/restart of the computer.  Note that merely
unloading the module does not invoke this profile....

Profile `recording` exists because I needed a LED profile to be able to switch to when the computer
is recording from my HDHomeRun cable box.  The module NEVER invokes the `recording` profile by itself,
due to no system events that trigger the profile.

Profile `voice` exists because I want my voice assistant program to turn the LED lights to particular
settings when it is listening.  The module NEVER invokes the `voice` profile by itself, due to no 
system events that trigger the profile.

While entering a set of profiles as a parameter, the module will stop processing the profile list if
an error is encountered during the processing of the string.  Any profiles past the point that
generated the error will not be processed.  The longest string you can pass to the module is 511 characters.

<hr>

## 8) Extra Notes

Once an LED has been set to `SW Control` in the BIOS, it will remain off initially until a color 
is explicitly set, after which the set color is retained across reboots.  This behavior is intentional
and can be changed by setting the `boot` and/or `shutdown` profiles.

If a caller calls the module at the same time another process is using it, the module will return a
`device or resource busy` error message.  This is because the module uses an internal buffer in
order to process input and output, and two processes using it at the time would corrupt the buffer.
It might cause the computer to crash, or worse yet, might cause a [buffer-overflow security issue](https://en.wikipedia.org/wiki/Buffer_overflow).

<hr>

## 9) Building the Module

The `nuc_led` kernel module supports building and installing "from source" directly or using `dkms`.

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
