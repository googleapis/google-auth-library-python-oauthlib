# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os.path
import tempfile

import click.testing
import google.oauth2.credentials
import mock
import pytest

import google_auth_oauthlib.flow
import google_auth_oauthlib.tool.__main__ as cli

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CLIENT_SECRETS_FILE = os.path.join(DATA_DIR, 'client_secrets.json')


class TestMain(object):
    @pytest.fixture
    def runner(self):
        return click.testing.CliRunner()

    @pytest.fixture
    def dummy_credentials(self):
        return google.oauth2.credentials.Credentials(
            token='dummy_access_token',
            refresh_token='dummy_refresh_token',
            token_uri='dummy_token_uri',
            client_id='dummy_client_id',
            client_secret='dummy_client_secret'
        )

    @pytest.fixture
    def local_server_mock(self, dummy_credentials):
        with mock.patch.object(google_auth_oauthlib.flow.InstalledAppFlow,
                               'run_local_server',
                               autospec=True) as flow:
            flow.return_value = dummy_credentials
            yield flow

    @pytest.fixture
    def console_mock(self, dummy_credentials):
        with mock.patch.object(google_auth_oauthlib.flow.InstalledAppFlow,
                               'run_console',
                               autospec=True) as flow:
            flow.return_value = dummy_credentials
            yield flow

    def test_help(self, runner):
        result = runner.invoke(cli.main, ['--help'])
        assert not result.exception
        assert '3LO OAuth2 flow' in result.output
        assert 'not intended for production' in result.output
        assert result.exit_code == 0

    def test_defaults(self, runner, dummy_credentials, local_server_mock):
        result = runner.invoke(cli.main, [
            '--client-secrets', CLIENT_SECRETS_FILE,
            '--scope', 'somescope',
        ])
        local_server_mock.assert_called_with(mock.ANY)
        assert not result.exception
        assert result.exit_code == 0
        creds_data = json.loads(result.output)
        assert creds_data['access_token'] == dummy_credentials.token
        assert creds_data['refresh_token'] == dummy_credentials.refresh_token
        assert creds_data['token_uri'] == dummy_credentials.token_uri
        assert creds_data['client_id'] == dummy_credentials.client_id
        assert creds_data['client_secret'] == dummy_credentials.client_secret

    def test_headless(self, runner, dummy_credentials, console_mock):
        result = runner.invoke(cli.main, [
            '--client-secrets', CLIENT_SECRETS_FILE,
            '--scope', 'somescope',
            '--headless'
        ])
        console_mock.assert_called_with(mock.ANY)
        assert not result.exception
        assert dummy_credentials.refresh_token in result.output
        assert result.exit_code == 0

    def test_save_new_dir(self, runner, dummy_credentials, local_server_mock):
        credentials_tmpdir = tempfile.mkdtemp()
        credentials_path = os.path.join(
            credentials_tmpdir,
            'new-directory',
            'credentials.json'
        )
        result = runner.invoke(cli.main, [
            '--client-secrets', CLIENT_SECRETS_FILE,
            '--scope', 'somescope',
            '--credentials-file', credentials_path,
            '--save'
        ])
        local_server_mock.assert_called_with(mock.ANY)
        assert not result.exception
        assert 'saved' in result.output
        assert result.exit_code == 0
        with open(credentials_path) as credentials_file:
            creds_data = json.load(credentials_file)
            assert 'access_token' not in creds_data
            creds = google.oauth2.credentials.Credentials(
                token=None, **creds_data
            )
            assert creds.token is None
            assert creds.refresh_token == dummy_credentials.refresh_token
            assert creds.token_uri == dummy_credentials.token_uri
            assert creds.client_id == dummy_credentials.client_id
            assert creds.client_secret == dummy_credentials.client_secret

    def test_save_existing_dir(self, runner, local_server_mock):
        credentials_tmpdir = tempfile.mkdtemp()
        result = runner.invoke(cli.main, [
            '--client-secrets', CLIENT_SECRETS_FILE,
            '--scope', 'somescope',
            '--credentials-file', os.path.join(
                credentials_tmpdir,
                'credentials.json'
            ),
            '--save'
        ])
        local_server_mock.assert_called_with(mock.ANY)
        assert not result.exception
        assert 'saved' in result.output
        assert result.exit_code == 0
