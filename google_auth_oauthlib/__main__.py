# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command line tool for fetching credentials using 3LO OAuth2 flow."""

import json
import os
import os.path

import click

import google_auth_oauthlib.flow


APP_NAME = 'google-oauthlib-tool'
DEFAULT_CREDENTIALS_FILENAME = 'credentials.json'


def credentials_flow_interactive(client_secrets_path, scopes, headless):
    """Initiate an interactive OAuth2InstalledApp flow.

    - If an X server is running: Run a browser based flow.
    - If not: Run a console based flow.

    Args:
      client_secrets_path(str): The path to the client secrets JSON file.
      scopes(Sequence[str]): The list of scopes to request during the flow.
      headless(bool): If True, run a console based flow otherwise run a web
      server based flow.

    Returns:
      google.oauth2.credentials.Credentials: new OAuth2 credentials authorized
        with the given scopes.

    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_path,
        scopes=scopes)
    if not headless:
        flow.run_local_server()
    else:
        flow.run_console()
    return flow.credentials


def credentials_to_dict(credentials):
    """Convert credentials to dict.

    Args:
      credentials(google.auth.credentials.Credentials): credentials to convert.

    Returns:
      dict: serializable credentials.
    """
    return {'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret}


@click.command()
@click.option('--client-secrets',
              metavar='<client_secret_json_file>', required=True,
              help='Path to OAuth2 client secret JSON file.')
@click.option('--scope', multiple=True,
              metavar='<oauth2 scope>', required=True,
              help='API scopes to authorize access for.')
@click.option('--save', is_flag=True,
              metavar='<save_mode>', show_default=True, default=False,
              help='Save the credentials to file.')
@click.option('--credentials-file',
              metavar='<oauth2_credentials_file>', show_default=True,
              default=os.path.join(
                  click.get_app_dir(APP_NAME),
                  DEFAULT_CREDENTIALS_FILENAME
              ),
              help='Path to store OAuth2 credentials.')
@click.option('--headless', is_flag=True,
              metavar='<headless_mode>', show_default=True, default=False,
              help='Run a console based flow.')
def main(client_secrets, scope, save, credentials_file, headless):
    """Helper script to generate OAuth2 credentials.
    """
    credentials = credentials_flow_interactive(client_secrets, scope, headless)
    credentials_data = credentials_to_dict(credentials)
    if save:
        config_path = os.path.dirname(credentials_file)
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
        with open(credentials_file, 'w') as f:  # pylint: disable=invalid-name
            json.dump(credentials_data, f)
        click.echo('credentials saved: %s' % credentials_file)
    else:
        click.echo(credentials_data)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
