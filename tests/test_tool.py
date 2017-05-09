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

import os.path

import google.oauth2.credentials
import mock

import google_auth_oauthlib.tool

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CLIENT_SECRETS_FILE = os.path.join(DATA_DIR, 'client_secrets.json')


def test_credentials():
    credentials = google.oauth2.credentials.Credentials(
        token=mock.sentinel.access_token,
        refresh_token=mock.sentinel.refresh_token,
        token_uri=mock.sentinel.token_uri,
        client_id=mock.sentinel.client_id,
        client_secret=mock.sentinel.client_secret)
    creds = google_auth_oauthlib.tool.credentials_to_dict(credentials)
    assert creds['access_token'] == mock.sentinel.access_token
    assert creds['refresh_token'] == mock.sentinel.refresh_token
    assert creds['token_uri'] == mock.sentinel.token_uri
    assert creds['client_id'] == mock.sentinel.client_id
    assert creds['client_secret'] == mock.sentinel.client_secret


class TestFlowInteractive(object):

    @mock.patch('google_auth_oauthlib.flow.InstalledAppFlow.run_console',
                autospec=True)
    def test_headless(self, run_console_mock):
        run_console_mock.return_value = mock.sentinel.credentials
        creds = google_auth_oauthlib.tool.credentials_flow_interactive(
            client_secrets_path=CLIENT_SECRETS_FILE,
            scopes=[],
            headless=True)
        run_console_mock.assert_called_with(mock.ANY)
        assert creds == mock.sentinel.credentials

    @mock.patch('google_auth_oauthlib.flow.InstalledAppFlow.run_local_server',
                autospec=True)
    def test_not_headless(self, run_local_server_mock):
        run_local_server_mock.return_value = mock.sentinel.credentials
        creds = google_auth_oauthlib.tool.credentials_flow_interactive(
            client_secrets_path=CLIENT_SECRETS_FILE,
            scopes=[],
            headless=False)
        run_local_server_mock.assert_called_with(mock.ANY)
        assert creds == mock.sentinel.credentials
