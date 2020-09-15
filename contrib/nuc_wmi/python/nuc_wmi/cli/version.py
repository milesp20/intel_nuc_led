"""
`nuc_wmi.cli.version` provides a CLI interface to the WMI version functions.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_FILE
from nuc_wmi.version import wmi_interface_spec_compliance_version

def wmi_interface_spec_compliance_version_cli():
    """
    Creates a CLI interface ontop of the `nuc_wmi.version` `wmi_interface_spec_compliance_version` function.

    Options:
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

    try:
        args = parser.parse_args()

        wmi_version = wmi_interface_spec_compliance_version(control_file=args.control_file)

        print(
            dumps(
                {
                    'version': {
                        'type': 'wmi_interface_spec_compliance',
                        'semver': '.'.join([str(semver_component) for semver_component in wmi_version])
                    }
                }
            )
        )
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)

    exit(0)
