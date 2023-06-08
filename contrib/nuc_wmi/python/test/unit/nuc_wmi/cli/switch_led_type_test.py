"""
The `test.unit.nuc_wmi.cli.switch_led_type_test` module provides unit tests for the functions in
`nuc_wmi.cli.switch_led_type`.

Classes:
    TestCliSwitchLedType: A unit test class for the functions in `nuc_wmi.cli.switch_led_type`.
"""

from __future__ import print_function

import json
import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.cli.switch_led_type import switch_led_type_cli
from nuc_wmi.switch_led_type import LED_COLOR_GROUP

import nuc_wmi


class TestCliSwitchLedType(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.switch_led_type`

    Methods:
        setUp: Unit test initialization.
        test_switch_led_type_cli: Tests that it returns the proper JSON response and exit code for
                                  valid cli args, tests that it captures raised errors and returns
                                  the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name

        self.nuc_wmi_spec = {
            'TEST_DEVICE': {
                'nuc_wmi_spec': {
                    'function_return_type': {
                        'switch_led_type': None
                    },
                    'recover': {
                        'function_oob_return_value': {
                            'switch_led_type': False
                        }
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.switch_led_type.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.switch_led_type.print')
    @patch('nuc_wmi.cli.switch_led_type.switch_led_type')
    @patch('nuc_wmi.cli.switch_led_type.sys.exit')
    def test_switch_led_type_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_switch_led_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `switch_led_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.switch_led_type.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.switch_led_type.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.switch_led_type.switch_led_type is \
                        nuc_wmi_switch_led_type)
        self.assertTrue(nuc_wmi.cli.switch_led_type.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that switch_led_type_cli returns the proper JSON response and exit
        #           code for valid cli args
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec

        returned_switch_led_type_cli = switch_led_type_cli([nuc_wmi_spec_alias, LED_COLOR_GROUP[0]])

        nuc_wmi_switch_led_type.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_COLOR_GROUP.index('Single color LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led_color_group': {
                    'type': LED_COLOR_GROUP[0]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_switch_led_type_cli, None)


    @patch('nuc_wmi.cli.switch_led_type.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.switch_led_type.print')
    @patch('nuc_wmi.cli.switch_led_type.switch_led_type')
    @patch('nuc_wmi.cli.switch_led_type.sys.exit')
    def test_switch_led_type_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_switch_led_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `switch_led_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.switch_led_type.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.switch_led_type.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.switch_led_type.switch_led_type is \
                        nuc_wmi_switch_led_type)
        self.assertTrue(nuc_wmi.cli.switch_led_type.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that switch_led_type_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_switch_led_type.side_effect = NucWmiError('Error (Function not supported)')

        returned_switch_led_type_cli = switch_led_type_cli([nuc_wmi_spec_alias, LED_COLOR_GROUP[0]])

        nuc_wmi_switch_led_type.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_COLOR_GROUP.index('Single color LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_switch_led_type_cli, None)
