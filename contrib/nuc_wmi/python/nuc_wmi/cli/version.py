"""
`nuc_wmi.cli.version` provides a CLI interface to the WMI version functions.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE
from nuc_wmi.version import wmi_interface_spec_compliance_version

import nuc_wmi

def wmi_interface_spec_compliance_version_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.version` `wmi_interface_spec_compliance_version` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with version and type or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the WMI interface spec compliance version or 1 on error.
    """

    parser = ArgumentParser(
        description='Get the WMI interface spec compliance version.'
    )

    parser.add_argument(
        '-c',
        '--control-file',
        default=None,
        help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Enable debug logging of read and write to the NUC LED control file to stderr.'
    )
    parser.add_argument(
        '-q',
        '--quirks',
        action='append',
        choices=nuc_wmi.QUIRKS_AVAILABLE,
        default=None,
        help='Enable NUC WMI quirks to work around various implementation issues or bugs.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        wmi_version = wmi_interface_spec_compliance_version(
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        wmi_semver = '.'.join([str(semver_component) for semver_component in wmi_version])

        print(
            dumps(
                {
                    'version': {
                        'type': 'wmi_interface_spec_compliance',
                        'semver': wmi_semver
                    }
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
