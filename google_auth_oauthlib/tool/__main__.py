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

"""Command-line tool for obtaining authorization and credentials from a user.

This tool uses the OAuth 2.0 Authorization Code grant as described in
`section 1.3.1 of RFC 6749`__ and implemeted by
:class:`google_auth_oauthlib.flow.Flow`.

This tool is intended to bootstrap development in situation when the
application cannot easily run the 3LO OAuth2 flow, i.e: in an embedded
device with limited input / display capabilities.

This is not intended for production where the main application should
run the 3LO OAuth2 flow to get authorization from the users.

..  __: https://tools.ietf.org/html/rfc6749#section-1.3.1
"""

import json
import os
import os.path

import click

import google_auth_oauthlib.flow


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
    """Command-line tool for obtaining authorization and credentials from a user.

    This tool uses the OAuth 2.0 Authorization Code grant as described
    in section 1.3.1 of RFC 6749:
    https://tools.ietf.org/html/rfc6749#section-1.3.1

    This tool is intended to bootstrap development in situation when the
    application cannot easily run the 3LO OAuth2 flow, i.e: in an embedded
    device with limited input / display capabilities.

    This is not intended for production where the main application should
    run the 3LO OAuth2 flow to get authorization from the users.
    """

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets,
        scopes=scope
    )
    if not headless:
        credentials = flow.run_local_server()
    else:
        credentials = flow.run_console()
    credentials_data = {
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret
    }

    if save:
        config_path = os.path.dirname(credentials_file)
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
        with open(credentials_file, 'w') as f:  # pylint: disable=invalid-name
            json.dump(credentials_data, f)
        click.echo('credentials saved: %s' % credentials_file)
    else:
        click.echo(json.dumps(credentials_data))


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
