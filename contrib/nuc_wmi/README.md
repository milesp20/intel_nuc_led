# nuc_wmi Python userland for Intel NUC LED kernel module

## Compatibility

This `nuc_wmi` userland was written from the merger of available Intel NUC WMI guides for the NUC 7, 8, and 10
(included in the [contrib/reference/](../reference) folder).

It has been tested on NUC 6, NUC 7 and 10, but theoretically should work for all NUCS from 6 through 10.

Although we followed the specification documents, we have found that compatibility varies by a number of factors:

* Device generation (NUC 7 devices for example only support the legacy `get_led` and `set_led` WMI methods).
* BIOS version (for some settings, the BIOS version may impact what options are available).
* BIOS configuration (for some settings, the BIOS configuration for LEDs can affect whether they are usable and
  in what default state they are in).
* BIOS bugs (we have found some device BIOS have bugs where LEDs which should support RGB are only capable of
  dual color mode through WMI, but are capable of RGB when manually configuring via BIOS).

Aside from the above, command options can change based on the combination of what the BIOS allows and what
indicator option mode LEDs are put in.

## Warnings

The `nuc_led` kernel module only allows return values for the last command issued to be read once. If multiple
commands are issued in rapid succession without reading the return code for each in between, then the return
codes are lost.

In the same light, there is an unresolved race condition in using the `nuc_wmi` userland as a result of this
behavior. Some of the CLI commands issue multiple WMI calls in succession in order to provide better usability
instead of just translating CLI options and blindly passing them into the WMI interface. Therefore, since we
haven't implemented file locking to prevent two CLI commands from creating a race condition on the control file,
we recommend not running CLI commands concurrently.

## Installing from package

On UBOS, these userland tools are part of the ``intel-nuc-led`` package. Install with:

```
sudo pacman -S ubos-nuc-led
```

On other distros, install from source.

## Installing from source

The tool conforms to standard Python `pip` packaging and can be installed using `pip` or `setuptools` using
Python >= `2.7`.

When installing from source using the instructions below, be sure to modify the `python` or `pip` executable
commands based on how you have your system setup as they may require appending the version to the end such
as `python2`, `python2.7`, `pip2`, or `pip2.7`.

### Installing from source using system `python`

#### Install using setuptools

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` Python package.
2. Install the `nuc-wmi` package using setuptools:
    ```
    python setup.py install
    ```
3. Run `nuc_wmi-*` commands available in `/usr/bin`.

#### Install using pip

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` and `pip` Python
   packages.
2. Install the package using setuptools or pip:
    ```
    # Install into the system Python library path
    python -m pip install ./

    # Install into the per user Python library path at `~/.local/`
    python -m pip install --user ./
    ```
3. Run `nuc_wmi-*` commands available in `/usr/bin` or `~/.local/bin/` (this may not automatically be in
   your `PATH`) if installed per user.

### Installing from source using `virtualenv`

You can install your own per user `python` and associated virtual library path using normal `virtualenv` tools or
wrappers like [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

Once you have your `virtualenv` setup, activate it and then follow the normal install steps above. When using a
`virtualenv` however, the library path and `bin` paths will be relative to the `virtualenv` parent directory.

## Packaging

The tool conforms to standard Python `pip` packaging using `setuptools` and can be turned into normal PyPi compatible
package in the form of a `wheel`, `egg`, or distro specific package using `setuptools` helpers.

### Python egg

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` Python package.
2. Build the `egg`:
    ```
    python setup.py build
    ```
3. The `egg` package is available in the `dist/` folder.

### Python wheel

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` and `wheel` Python
   packages.
2. Build the `wheel`:
    ```
    python setup.py build bdist_wheel
    ```
3. The `wheel` package is available in the `dist/` folder.

### Debian/Ubuntu deb

1. Use `apt` to install your choice of `python` version and `setuptools` and `stdeb` Python packages.
2. Use `apt` to install `debhelper` and `fakeroot`.
2. Build the `deb`:
    ```
    DEB_BUILD_OPTIONS=nocheck python setup.py --command-packages=stdeb.command bdist_deb
    ```
3. The `deb` package is available in the `dist/` folder.

## Testing

Use your system's package manager to install your choice of `python` version and `coverage`, `mock`, `nose`, `nose-cov`,
`pylint`, and `setuptools` Python packages.

Clean directory:

```
rm -rf .coverage build/ deb_dist/ dist/ python/cover python/nuc_wmi.egg-info nuc_wmi-*.tar.gz
find . -type f -name "*~" -exec rm {} +
find . -type f -name "*.pyc" -exec rm {} +
find . -type d -name "__pycache__" -exec rmdir {} +
```

Run tests:

```
pylint python/nuc_wmi python/test/
python setup.py test
```

Run detailed code coverage report (HTML report available in `python/cover/`):

```
python setup.py nosetests --cover-branches --cover-html --cover-html-dir ./cover --cover-package nuc_wmi -d -s -v --with-coverage --py3where python/
```

## Example Usage

All `nuc_wmi-*` CLI commands provided by `nuc_wmi` Python module have builtin help via `-h` or `--help` and will
show allowed argument values. Some commands allow a large number of combinations in terms of accepted input values,
so please be sure to reference the WMI spec for the device you are using to see what is actually supported.

### NUC 7:

```
# Note: When a legacy device (NUC 7 or older) has disabled software control in BIOS, we can't change it
# via WMI like we can on newer models. Trying to use a LED that hasnt had software control enabled will return
# this error.
$ nuc_wmi-get_led 'S0 Power LED'
{"error": "Error (Undefined device)"}

$ nuc_wmi-get_led 'S0 Ring LED'
{"led": {"color": "White", "frequency": "Always on", "type": "S0 Ring LED", "brightness": "100"}}

# Brightness is an integer percentage 0-100 and not the internal WMI hex value.
$ nuc_wmi-set_led 'S0 Ring LED' 100 'Always on' 'White'
{"led": {"color": "White", "frequency": "Always on", "type": "S0 Ring LED", "brightness": "100"}}
```

### NUC 10:

```
$ nuc_wmi-get_led_control_item 'HDD LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}}
# For BIOS where the HDD LED LED color type is "Dual-color Blue / White"
$ nuc_wmi-get_led_control_item 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}}
$ nuc_wmi-get_led_control_item 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}}
$ nuc_wmi-get_led_control_item 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "50"}}
$ nuc_wmi-get_led_control_item 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}}

$ nuc_wmi-get_led_indicator_option 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}}
$ nuc_wmi-get_led_indicator_option 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}}

$ nuc_wmi-query_led_color_type 'HDD LED'
{"led": {"color_type": "Dual-color Blue / White", "type": "HDD LED"}}
$ nuc_wmi-query_led_color_type 'Power Button LED'
{"led": {"color_type": "Dual-color Blue / Amber", "type": "Power Button LED"}}
$ nuc_wmi-query_led_color_type 'HDD LED'
{"led": {"color_type": "RGB-color", "type": "HDD LED"}}

$ nuc_wmi-query_led_control_items 'Power Button LED' 'Power State Indicator'
{"led": {"control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color"], "type": "Power Button LED", "indicator_option": "Power State Indicator"}}
$ nuc_wmi-query_led_control_items 'Power Button LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "Power Button LED", "indicator_option": "Software Indicator"}}
$ nuc_wmi-query_led_control_items 'HDD LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "HDD LED", "indicator_option": "Software Indicator"}}
$ nuc_wmi-query_led_control_items 'HDD LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Color 2", "Color 3"], "type": "HDD LED", "indicator_option": "HDD Activity Indicator"}}

$ nuc_wmi-query_led_indicator_options 'HDD LED'
{"led": {"type": "HDD LED", "indicator_options": ["HDD Activity Indicator", "Software Indicator"]}}
$ nuc_wmi-query_led_indicator_options 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}}

# RGB Header is only available if on the latest BIOS
$ nuc_wmi-query_leds
{"leds": ["Power Button LED", "HDD LED", "RGB Header"]}

$ nuc_wmi-save_led_config
{"led_app_notification": {"type": "save_led_config"}}

# Brightness is an integer percentage 0-100 and not the internal WMI hex value.
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}}
# Blinking Frequency is 0.1Hz-1.0Hz
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}}
$ nuc_wmi-set_led_control_item 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Blue
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}}
# For BIOS where the HDD LED LED color type is "RGB-color" but 1D (where only 'Color' is a supported control item)
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Color' 'Indigo'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Indigo"}}
# For LEDs where the color type is RGB-color but 3D, the color is controlled by 3 dimension settings (one for Red, Green, and Blue respectively) that accept
# an integer value from 0-255 for each color dimension. There may be multiple control item triplets for RGB colors per indicator option. For
# this example we pretend the HDD LED reports its color type as RGB-color and we set the LED to Red (you must set all 3 dimensions to ensure you end up with the correct color).
# If you want to avoid having the color change as you set the dimensions, your only option is to drop the brightness down to 0 before settng the color and back to a
# non zero brightness once its set.
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Color' '255' # Red dimension
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "255"}}
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Color 2' '0' # Green dimension
{"led": {"control_item": "Color 2", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0"}}
$ nuc_wmi-set_led_control_item 'HDD LED' 'Software Indicator' 'Color 3' '0' # Blue dimension
{"led": {"control_item": "Color 3", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0"}}

$ nuc_wmi-set_led_indicator_option 'HDD LED' 'Software Indicator'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}}
$ nuc_wmi-set_led_indicator_option 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}}

# No idea what this WMI function does, I just implemented it according to spec. It doesnt work on NUC 10.
$ nuc_wmi-switch_led_type 'Single color LED'
$ nuc_wmi-switch_led_type 'Multi color LED'

$ nuc_wmi-wmi_interface_spec_compliance_version
{"version": {"semver": "1.32", "type": "wmi_interface_spec_compliance"}}
```
## Quirks Mode

Unfortunately there can be a large set of differences across the devices and sometimes bugs in the BIOS
implementation make it out into the wild. All CLI commands support `quirks mode` via the `-q` and `--quirks`
CLI options.

### NUC 7 Quirks

* `NUC7_FREQUENCY_DEFAULT`: This `quirks mode` changes the processing of the return value for the `get_led`
    WMI method for NUC 7 BIOS. This affects NUC 7 in a factory default state where the NUC LEDs state hasnt been changed.
    In a factory default state, the NUC 7 can properly return `0` for `brightness` and `0` for `color` (aka `Disabled`),
    however it also returns `0` for `frequency` which is an invalid enum value according to the documentation. Enabling
    this quirks mode overrides any `0` value returned for `frequency` and converts it to `1` for `1Hz`. Enabling this
    quirks mode on a BIOS not affected by this issue will not cause a change in the return value for `frequency`.

### NUC 10 Quirks

* `NUC10_RETURN_VALUE`: This `quirks mode` changes the processing of the return value for the `query_led_color_type`
    and `get_led_indicator_option` WMI methods for NUC 10 BIOS released before December 2020 that also did not support
    the NUC 10 RGB header. In NUC 10 BIOS released before December 2020, the implementation for these two WMI methods do
    not follow the spec, therefore they are only compatible `nuc_wmi` `1.0`. If you have the December 2020 or later BIOS,
    then `nuc_wmi` `1.1` or later is required. `nuc_wmi` `2.1` was the first version to support this `quirks mode` so
    any version `2.1` or greater supports all these BIOS.

    In order to determine whether or not you need to enable this `quirks mode`, you can run `nuc_wmi-query_leds` and
    if `RGB Header` is not an option then you will likely have to enable this `quirk`. Note that although only
    `query_led_color_type` and `get_led_indicator_option` WMI method's return value processing is affected, some of the
    other `nuc_wmi` CLI functions may call these two functions when processing CLI arguments, therefore you should always
    enable this `quirks mode` if your BIOS version is old enough to be affected by it.
