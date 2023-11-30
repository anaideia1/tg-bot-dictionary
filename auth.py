import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-translation",
]


def get_credentials_from_file(
        credentials_file: str = 'credentials.json'
) -> Credentials:
    """
    Create GCP OAuth credentials from file and, if needed, refresh tokens
    :param credentials_file: name of file, where GCP OAuth credentials stored
    :return: google.oauth2.credentials.Credentials created from file
    """
    dir_path = os.path.dirname(__file__)
    token_file = os.path.join(dir_path, 'token.json')
    credentials_file = os.path.join(dir_path, credentials_file)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds
