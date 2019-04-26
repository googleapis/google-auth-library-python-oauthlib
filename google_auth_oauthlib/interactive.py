# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Get user credentials from interactive code environments.

This module contains helpers for getting user credentials from interactive
code environments installed on a development machine, such as Jupyter
notebooks.
"""

from __future__ import absolute_import

import google_auth_oauthlib.flow


_CLIENT_ID = "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com"
_CLIENT_SECRET = "d-FL95Q19q7MQmFpd7hHD0Ty"


def get_user_credentials(scopes):
    """Gets credentials associated with your Google user account.

    This function authenticates using your user credentials by going through
    the OAuth 2.0 flow. You'll open a browser window asking for you to
    authenticate to your Google account using authentication library. The
    permissions it requests correspond to the scopes you've provided.

    .. warning::
        If you are writing an application, tool, or library which accesses
        Google APIs, use the :mod:`google_auth_oauthlib.flow` module directly
        and supply client information identifying your application. You are
        `required by the Google APIs terms of service
        <https://developers.google.com/terms/#c_permitted_access>`__ to
        accurately identify your application.

    Args:
        scopes (Sequence[str]):
            A list of scopes to use when authenticating to Google APIs. See
            the `list of OAuth 2.0 scopes for Google APIs
            <https://developers.google.com/identity/protocols/googlescopes>`_.

    Returns:
        google.oauth2.credentials.Credentials:
            The OAuth 2.0 credentials for the user.
    """

    client_config = {
        "installed": {
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    }

    app_flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=scopes
    )

    return app_flow.run_console()
