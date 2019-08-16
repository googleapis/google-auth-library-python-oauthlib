import json
import os

import google.auth
from google.oauth2.credentials import Credentials
import google.oauth2.id_token
from google.oauth2.file import Storage

from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow


_APP_JSON_FILE_NOT_FOUND_MESSAGE = 'OAuth app credentials file {} not found'


class LoadSaveCredsFlow:
    """Automates the OAuth login flow. This entails loading saved credentials
    from file, running the OAuth flow if needed, saving credentials to file,
    and providing a Google API service as a class property.

    Provided properties and methods:
        API:                        the Google API service object
        get_user_email_address:     returns the email address of the authorised
                                    credentials
    """

    def __init__(self,
                 storage_file,
                 app_json_file,
                 scopes,
                 service,
                 version,
                 interactive=True):
        """
        Args:
            storage_file (str):   file that should contain the user credentials
            app_json_file (str):  file that contains the OAuth app credentials
            scopes (list of str): list of Google scopes that should be used
                                  when creating the API service objet
            service (str):        Google API service name
            version (str):        Google API service version
            interactive (bool):   True uses the slightly more interactive CLI
                                  authentication method, False uses the simpler
                                  copy/paste method
        """
        # The app_json_file file is essential, script must fail without it
        if not os.path.isfile(app_json_file):
            raise FileNotFoundError(
                    _APP_JSON_FILE_NOT_FOUND_MESSAGE.format(app_json_file))

        # Try and load stored credentials. If it fails, run the OAuth flow
        try:
            self._credentials = Credentials.from_authorized_user_file(
                    storage_file)
        except (json.JSONDecodeError, FileNotFoundError):
            flow = InstalledAppFlow.from_client_secrets_file(
                    app_json_file,
                    scopes=scopes)
            if interactive is True:
                self._credentials = flow.run_local_server()
            elif interactive is False:
                self._credentials = flow.run_console()

            # Save the freshly acquired credentials
            store = Storage(storage_file)
            store.put(self._credentials)

        # Build the Google API object
        self._API = build(service, version, credentials=self._credentials)

    @property
    def API(self):
        """The Google API service object. Returns `self._API`.
        """
        return self._API

    def get_user_email_address(self):
        """Returns the OAuth's token email address. This will only work
        if the following scopes are present in the scope list when the access
        is initially granted:
                https://www.googleapis.com/auth/userinfo.email
                openid

        Returns:
            Email address of the stored OAuth credential as a string
        """
        try:
            request = google.auth.transport.requests.Request()
            self._credentials.refresh(request)
            decodedIDtoken = google.oauth2.id_token.verify_oauth2_token(
                    self._credentials.id_token,
                    request)
            return decodedIDtoken['email']
        except ValueError:
            return None
