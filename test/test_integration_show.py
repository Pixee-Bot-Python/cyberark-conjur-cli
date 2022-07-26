# -*- coding: utf-8 -*-

"""
CLI Show Integration tests
This test file handles the main test flows for the show command
"""
from contextlib import redirect_stderr
import io
import os
from unittest.mock import patch

from conjur.constants import LOGIN_IS_REQUIRED
from test.util.test_infrastructure import integration_test
from test.util.test_runners.integration_test_case import IntegrationTestCaseBase
from test.util import test_helpers as utils


# Not coverage tested since integration tests don't run in
# the same build step
class CliIntegrationTestShow(IntegrationTestCaseBase):  # pragma: no cover
    capture_stream = io.StringIO()
    defined_variable_id='one/password'
    expected_output = '"id": "dev:variable:one/password",\n    "owner": "dev:user:admin",\n    "policy": "dev:policy:root",\n    "permissions": []'

    def __init__(self, testname, client_params=None, environment_params=None):
        super(CliIntegrationTestShow, self).__init__(testname, client_params, environment_params)

    # *************** HELPERS ***************

    def setUp(self):
        self.setup_cli_params({})
        # Used to configure the CLI and login to run tests
        utils.setup_cli(self)
        return self.invoke_cli(self.cli_auth_params,
                               ['policy', 'replace', '-b', 'root', '-f', self.environment.path_provider.get_policy_path("show")])

    # *************** TESTS ***************

    @integration_test()
    def test_show_get_insecure_prints_warning_in_log(self):
        with self.assertLogs('', level='DEBUG') as mock_log:
            self.invoke_cli(self.cli_auth_params,
                                     ['--insecure', 'show', '-i', f'variable:{self.defined_variable_id}'])
            self.assertIn("Warning: Running the command with '--insecure' makes your system vulnerable to security attacks",
                          str(mock_log.output))

    @integration_test()
    def test_show_without_id_returns_help(self):
        with redirect_stderr(self.capture_stream):
            self.invoke_cli(self.cli_auth_params,
                            ['show'], exit_code=1)
        self.assertIn("Error the following arguments are required:", self.capture_stream.getvalue())

    @integration_test(True)
    def test_show_short_with_help_returns_show_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-h'])
        self.assertIn("Name:\n  show", output)

    @integration_test(True)
    def test_show_long_with_help_returns_show_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '--help'])
        self.assertIn("Name:\n  show", output)

    @integration_test(True)
    def test_show_long_resource_id_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', f'--id=variable:{self.defined_variable_id}'])
        self.assertIn(self.expected_output, output)

    @integration_test(True)
    def test_show_short_resource_id_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', f'variable:{self.defined_variable_id}'])
        self.assertIn(self.expected_output, output)

    @integration_test(True)
    def test_show_resource_id_with_account_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', f'dev:variable:{self.defined_variable_id}'])
        self.assertIn(self.expected_output, output)

    @integration_test(True)
    def test_show_policy_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:policy:root'])
        self.assertIn('"id": "dev:policy:root"', output)

    @integration_test(True)
    def test_show_user_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:user:someuser'])
        self.assertIn('"id": "dev:user:someuser"', output)

    @integration_test(True)
    def test_show_layer_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:layer:somelayer'])
        self.assertIn('"id": "dev:layer:somelayer"', output)

    @integration_test(True)
    def test_show_group_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:group:somegroup'])
        self.assertIn('"id": "dev:group:somegroup"', output)

    @integration_test(True)
    def test_show_host_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:host:anotherhost'])
        self.assertIn('"id": "dev:host:anotherhost"', output)

    @integration_test(True)
    def test_show_webservice_returns_resource(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'dev:webservice:somewebservice'])
        self.assertIn('"id": "dev:webservice:somewebservice"', output)

    @integration_test(True)
    def test_unknown_resource_raises_not_found_error(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['show', '-i', 'variable:unknown'], exit_code=1)
        self.assertIn("404 (Not Found) for url:", output)

    '''
    Validates that when the user isn't logged in and makes a request,
    they are prompted to login first and then the command is executed
    '''
    @integration_test()
    @patch('builtins.input', return_value='admin')
    def test_show_without_user_logged_in_prompts_login_and_performs_show(self, mock_input):
        # TEST_ENV is set to False so we will purposely be prompted to login
        os.environ['TEST_ENV'] = 'False'
        try:
            utils.delete_credentials()
        except OSError:
            pass

        with patch('getpass.getpass', return_value=self.client_params.env_api_key):
            output = self.invoke_cli(self.cli_auth_params,
                                     ['show', '-i', f'variable:{self.defined_variable_id}'])

            self.assertIn(LOGIN_IS_REQUIRED, output)
            self.assertIn("Successfully logged in to Conjur", output)
            self.assertIn(self.expected_output, output)
        os.environ['TEST_ENV'] = 'True'
