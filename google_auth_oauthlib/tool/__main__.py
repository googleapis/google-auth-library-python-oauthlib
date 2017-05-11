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

"""Command line tool for fetching credentials using 3LO OAuth2 flow.
"""

import json
import os
import os.path

import click

from google_auth_oauthlib.tool import (
    credentials_flow_interactive,
    credentials_to_dict
)


APP_NAME = 'google-oauthlib-tool'
DEFAULT_CREDENTIALS_FILENAME = 'credentials.json'


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
    """Command line tool for fetching credentials using 3LO OAuth2 flow.

    This tool is intended to bootstrap development in situation when the
    application cannot easily run the 3LO OAuth2 flow, i.e: in an embedded
    device with limited input / display capabilities.

    This is not intended for production where the main application should
    run the 3LO OAuth2 flow to get authorization from the users.
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
