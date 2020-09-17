# nuc_wmi Python userland for Intel NUC LED kernel module

## Compatibility

This `nuc_wmi` userland was written from the merger of available Intel NUC WMI guides for the NUC 7, 8, and 10 (included in the `contrib/reference/` folder).

It has been tested on NUC 7 and 10, but theoretically should work for NUC 6 through 10.

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

Making a debian package (requires `stdeb` python package and should be done directly on the same system it is targeting):

```
make deb
```
