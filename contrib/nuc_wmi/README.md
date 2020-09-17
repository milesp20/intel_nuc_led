# nuc_wmi Python userland for Intel NUC LED kernel module

## Compatibility

This `nuc_wmi` userland was written from the merger of available Intel NUC WMI guides for the NUC 7, 8, and 10
(included in the `contrib/reference/` folder).

It has been tested on NUC 7 and 10, but theoretically should work for NUC 6 through 10.

Although we followed the specification documents, we have found that compatibility varies by a number of factors:

* Device generation (NUC 7 devices for example only support the legacy `get_led` and `set_led` WMI methods).
* BIOS version (For some settings, the BIOS version may impact what options are available).
* BIOS configuration (For some settings, the BIOS configuration for LEDs can affect whether they are usable and
  in what default state they are in).
* BIOS bugs (We have found some device BIOS have bugs where LEDs which should support RGB are only capable of
  dual color mode through WMI, but are capable of RGB when manually configuring via BIOS).

Aside from the above, command options can change based on the combination of what the BIOS allows and what
indicator option mode LEDs are put in.

## Warnings

The `nuc_led` kernel module only allows return values for the last command issued to be read once. If multiple
commands are issued in rapid succession without reading the return code for each in between, then the return
codes are lost.

In the same light, there is an unresolved race condition in using the `nuc_wmi` userland as a result of this
behavior. Some of the CLI commands issue multiple WMI calls in succession in order to provide better usability
instead of just translating CLI options and blinding passing them into the WMI interface. Therefore, since we
haven't implement file locking to prevent two CLI commands from creating a race condition on the control file,
we recommend not running CLI commands concurrently.

## Testing

Clean directory:

```
make clean
```

Run tests:

```
make test
```

Run detailed code coverage report (HTML report available in `python/cover/`):

```
make nosetests
```

## Building

Making a Debian package (requires `stdeb` python package and should be done directly on the same system it
is targeting):

```
make deb
```
