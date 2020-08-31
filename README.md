# Intel NUC LED Control: NUC6CAY, NUC7i[x]BN and NUC10i3FNH, maybe more

This is a simple kernel module to control LEDs on Intel NUCs.

It is based on the previous work at
[github.com/milesp20/intel_nuc_led](https://github.com/milesp20/intel_nuc_led/), but
with significant changes:

* it can be used with the more recent NUC10 as well
* it tracks the more recent kernel APIs
* currently it is very low-level, and you'll be sending and receiving bytes
* higher-level commands like "turn the power LED to flashing red" are not
  implemented in the kernel module itself.

This was primarily created for [UBOS](https://ubos.net/), a Linux distro for
self-hosting (based on Arch) and is mostly tested there. But chances are you
can run it on other distros as well.

Pull requests appreciated. And reports if you could (or could not) get it
running on other NUCs with software-controllable LEDs, and other distros.

## Requirements

Requirements:

* Intel NUC6CAY, or NUC7i[x]BN or NUC10i3FNH, maybe more
* BIOS AY0038 or BN0043 or later
* ACPI/WMI support in kernel
* LED(s) set to `SW Control` in BIOS

## Building

THe `nuc_led` kernel module supports building and installing "from source" directly or using `dkms`.

### Installing Build Dependencies

UBOS:
```
pacman -S linux-headers base-develop
```

Ubuntu (not verified):

```
apt-get install build-essential linux-headers-$(uname -r)

# DKMS dependencies
apt-get install debhelper dkms
```

Redhat (not verified):

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
# UBOS
makepkg

# Ubuntu (not verified)
make dkms-deb

# RHEL (not verified)
make dkms-rpm

# Install generated DEB/RPM from the folder specified in the output using system package manager
```

## Low-level vs high-level interface

In the previous, NUC6/NUC7-only version by milesp20, you would use something like:

```
echo 'ring,80,blink_medium,green' > /proc/acpi/nuc_led
```

to turn the ring LED to a blinking green. But with the greater hardware
variety now supported by this module, and a substantially extended number
of API calls, this interface doesn't make so much sense any more. In
addition, some settings now require several system calls.

So instead we simply expose the input and outputs of the WMI system call,
and leave it to the user to send in the right bytes, and interpret the
resulting bytes.

Maybe somebody wants to design some higher-level tools to make this easier?
As a bonus, those tools could run in userspace.

## Usage (Kernel device)

NOTE: this works differently from the previous version by milesp20.

```
echo xx xx xx xx xx > /proc/acpi/nuc_led
```
where the ``xx`` are 1-byte hex numbers:

* first byte: the Method ID of the WMI call
* bytes 2-5: the four bytes of arguments passed into the WMI call

This will invoke the specified method with the provided arguments,
and save the return results.

And then:

```
cat /proc/acpi/nuc_led
```
will emit 4 hex numbers, which are the bytes returned by the last
invocation of the WMI system call.

## The bytes and their values

The following Intel documents describe the available Method IDs and
parameters:

* for the NUC6CAY, or NUC7i[x]BN:
  [Use WMI Explorer* to Program the Ring LED and Button LED](https://www.intel.com/content/www/us/en/support/articles/000023426/intel-nuc/intel-nuc-kits.html)

* for the NUC10i3FNH:
  [WMI Interface for Intel NUC Products / WMI Specification / Frost Canyon / July2020 Revision 1.0](https://www.intel.com/content/dam/support/us/en/documents/intel-nuc/WMI-Spec-Intel-NUC-NUC10ixFNx.pdf)

Note that the WMI APIs have changed significantly. E.g. the Method IDs
for the older models are 1 and 2, while the they are 3 to 9 for the newer
model.

## Errors

Errors will appear as warnings in dmesg or journalctl -k. WMI call
error codes are part of the return value of the WMI call, and shown
through ``cat /proc/acpi/nuc_led``.

## Examples

### NUC6CAY

Make sure you have enabled LED software control in the BIOS:

To set the Ring LED to brightness 80, blink at medium speed, and green:

```
echo 02 02 50 05 06 > /proc/acpi/nuc_led
```

where:
* `02`: method ID: "Set LED function"
* `02`: Ring LED command mode
* `50`: 80% brightness (in hex)
* `05`: 0.5 Hz
* `06`: green

### NUC10i3FNH

Make sure you have enabled LED software control in the BIOS:

To set the Power Button LED to brightness 80, blink at medium speed, and color amber:

```
echo 06 00 04 00 50 > /proc/acpi/nuc_led # brightness
echo 06 00 04 01 02 > /proc/acpi/nuc_led # blinking behavior
echo 06 00 04 02 05 > /proc/acpi/nuc_led # blinking frequency
echo 06 00 04 03 01 > /proc/acpi/nuc_led # color

```

where:

* brightness:

  * `06`: method ID: "Set the value to the control item of the indicator option and the LED type"
  * `00`: power button LED
  * `04`: software indicator
  * `00`: brightness control item
  * `50`: brightness value (in hex)

* blinking behavior (same, then):

  * `01`: blinking behavior control item
  * `02`: pulsing

* blinking frequency (same, then):

  * `02`: blinking behavior control item
  * `05`: 5 times 0.1Hz = 0.5Hz

* color (same, then):

  * `03`: color control item
  * `01`: amber color

## Permissions

You can change the owner, group and permissions of `/proc/acpi/nuc_led` by
passing parameters to the nuc_led kernel module. Use:

* `nuc_led_uid` to set the owner (default is 0, root)
* `nuc_led_gid` to set the owning group (default is 0, root)
* `nuc_led_perms` to set the file permissions (default is r+w for
  group and user and r for others)

Note: Once an LED has been set to `SW Control` in the BIOS, it will
remain off initially until a color is explicitly set, after which the set
color is retained across reboots.
