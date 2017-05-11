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

import google_auth_oauthlib.flow


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
        return flow.run_local_server()
    else:
        return flow.run_console()


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
