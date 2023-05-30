"""
`nuc_wmi.cli.version` provides a CLI interface to the WMI version functions.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE, LOCK_FILE
from nuc_wmi.utils import acquire_file_lock, load_nuc_wmi_spec
from nuc_wmi.version import wmi_interface_spec_compliance_version


def wmi_interface_spec_compliance_version_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.version` `wmi_interface_spec_compliance_version` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with version and type or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the WMI interface spec compliance version or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Get the WMI interface spec compliance version.'
        )

        parser.add_argument(
            '-b',
            '--blocking-file-lock',
            action='store_true',
            help='Acquire a blocking lock on the NUC WMI lock file instead of the default non blocking lock.'
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
            '-l',
            '--lock-file',
            default=None,
            help='The path to the NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )
        parser.add_argument(
            'nuc_wmi_spec_alias',
            choices=nuc_wmi_spec['nuc_wmi_spec'].keys(),
            help='The name of the NUC WMI specification to use from the specification configuration file.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file, blocking_file_lock=args.blocking_file_lock)

            wmi_version = wmi_interface_spec_compliance_version(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            wmi_semver = '.'.join([str(semver_component) for semver_component in wmi_version])

            print(
                dumps(
                    {
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias,
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
