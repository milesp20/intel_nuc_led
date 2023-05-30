# Intel NUC WMI kernel driver and Python userland CLI tools

This is a simple kernel module that serves as an RPC interface for internal WMI functions
on Intel NUCs through a control file leveraging the Linux kernel /proc tree with
optional high-level userspace tools written in Python.

The current `2.0` version of the kernel driver is backwards incompatible with the original `1.0`
version which only supported NUC 6 and 7. Reference the
[old documentation](https://github.com/milesp20/intel_nuc_led/tree/6a3850eadff554053ca7d95e830a624b28c53670)
for `1.0` usage.

Please be aware that while this repo was originally intended to control the NUC LED, the driver has
now been renamed to be generic and not specific to the LED now that its a low level interface to the WMI
functions since some NUC models also support controlling the HDMI and USB bus via other WMI functions. We
currently do not implement CLI helper methods for those and only support the NUC LED WMI functions in the
current userland.

Pull requests appreciated as well reports if you could (or could not) get it
running on other NUCs with software-controllable LEDs, and other distros.

## Known Issues

* Currently, 5.x kernels in Ubuntu 20.04 and 22.04 appear to be have problems (unknown if its a bug in the
  kernel module itself or the kernels) with using Python to read from the control file in a buffered I/O manner.

  As of `nuc_wmi` CLI `3.0.1`, we work around this issue by reading/writing to the control file using unbuffered
  I/O.
* Performance of the NUC WMI methods is severely degraded in NUC 12s and is about 20-100x slower for some WMI
  methods than previously on the NUC 10. This is a BIOS issue that we cant work around due to a delayed response.

## Requirements

Requirements:

* Intel NUC 6 through 12
* ACPI/WMI support in kernel

## LED Header Breakout Boards

Example NUC LED header breakout boards for internal LED headers are available in
[contrib/led_header_boards](contrib/led_header_boards).

## Building the kernel module

The `nuc_wmi` kernel module supports building and installing "from source" directly or using `dkms`.

### Installing Build Dependencies

UBOS: you don't need to, it's in the repos: `pacman -S intel-nuc-wmi`

If you want to build it anyway, you need:

```
pacman -S linux-headers base-develop
```

Ubuntu:

```
apt-get install build-essential linux-headers-$(uname -r)

# DKMS dependencies
apt-get install debhelper dkms fakeroot
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

You can override the `KVERSION` or `KDIR` environment variables to customize the build as needed.

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
makepkg -i

# Ubuntu
make dkms-deb

# RHEL
make dkms-rpm

# Install generated DEB/RPM from the folder specified in the output using system package manager
```

## Low-level vs high-level interface

### High-level Python Userland CLI

See [Python nuc_wmi userland](contrib/nuc_wmi) documentation for NUC WMI CLI commands. We recommend using this interface over
using the low lowel control file directly for ease of use.

### Low-level Control File Usage (Kernel device)

```
echo xx xx xx xx xx > /proc/acpi/nuc_wmi
```
where the `xx` are 1-byte hex numbers:

* first byte: the Method ID of the WMI call
* bytes 2-5: the four bytes of arguments passed into the WMI call

This will invoke the specified method with the provided arguments,
and save the return results.

And then:

```
cat /proc/acpi/nuc_wmi
```
will emit 4 hex numbers, which are the bytes returned by the last
invocation of the WMI system call.

### Low-level Control File bytes and their values

The following Intel documents describe the available Method IDs and
parameters:

* for the NUC6CAY, or NUC7i[x]BN:
  [Use WMI Explorer* to Program the Ring LED and Button LED](https://www.intel.com/content/www/us/en/support/articles/000023426/intel-nuc/intel-nuc-kits.html).

* for the NUC10i3FNH:
  [WMI Interface for Intel NUC Products / WMI Specification / Frost Canyon / July2020 Revision 1.0](https://www.intel.com/content/dam/support/us/en/documents/intel-nuc/WMI-Spec-Intel-NUC-NUC10ixFNx.pdf)

There are copies of these documents here in [contrib/reference](contrib/reference/).

Note that the WMI functions have changed significantly. E.g. the Method IDs
for the older models are 1 and 2, while the they are 3 to 9 for the newer
model.

### Low-level Control File Errors

Errors will appear as warnings in `dmesg` or `journalctl -k`. WMI call
error codes are part of the return value of the WMI call, and shown
through `cat /proc/acpi/nuc_wmi`.

Once the device has been read, the value there will be reset to
`ff ff ff ff` (something not used by the WMI call). This is also the
initial value.

## Examples

### NUC6CAY

Make sure you have enabled LED software control in the BIOS, as there
is no WMI call to change that setting on this device.

To set the Ring LED to brightness 80, blink at medium speed, and green:

```
echo 02 02 50 05 06 > /proc/acpi/nuc_wmi
```

where:
* `02`: method ID: "Set LED function"
* `02`: Ring LED command mode
* `50`: 80% brightness (in hex)
* `05`: 0.5 Hz
* `06`: green

### NUC10i3FNH

Make sure you have enabled LED software control in the BIOS, or have
previously executed the WMI call to turn on software control.

To set the Power Button LED to brightness 80, blink at medium speed, and color amber:

```
echo 06 00 04 00 50 > /proc/acpi/nuc_wmi # brightness
echo 06 00 04 01 02 > /proc/acpi/nuc_wmi # blinking behavior
echo 06 00 04 02 05 > /proc/acpi/nuc_wmi # blinking frequency
echo 06 00 04 03 01 > /proc/acpi/nuc_wmi # color
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

You can change the owner, group and permissions of `/proc/acpi/nuc_wmi` by
passing parameters to the kernel module. Use:

* `nuc_wmi_uid` to set the owner (default is 0, root)
* `nuc_wmi_gid` to set the owning group (default is 0, root)
* `nuc_wmi_perms` to set the file permissions (default is r+w for
  group and user and r for others)
