from __future__ import print_function

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.protobuf import service
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1I1n25GcTDe7jtDJ7nV0-8pOErjFfDsn5YpNSHq8qtKk'


def input_doc(str_import, channel_name, bold_list, ital_list):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        print('The title of the document is: {}'.format(document.get('title')))
    except HttpError as err:
        print(err)

    # creating the doc
    service = build('docs', 'v1', credentials=creds)
    body = {
        'title': channel_name + " (" + time.strftime(format("%m/%d/%Y")) + ")"
    }
    doc = service.documents().create(body=body).execute()
    docID = doc.get('documentId')

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': str_import
            }
        }
    ]
    # editing the doc and adding the conversation text
    adding = service.documents().batchUpdate(documentId=docID, body={'requests': requests}).execute()

    # editing the text to make the username bold
    formattingList = []
    for b in bold_list:
        formattingList.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': b[0] + 1,
                    'endIndex': b[1] + 1
                },
                'textStyle': {
                    'bold': True
                },
                'fields': 'bold'
            }
        })
    adding = service.documents().batchUpdate(documentId=docID, body={'requests': formattingList}).execute()

    # editing the text to make date/time italic
    formattingList = []
    for i in ital_list:
        formattingList.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': i[0] + 1,
                    'endIndex': i[1] + 1
                },
                'textStyle': {
                    'italic': True
                },
                'fields': 'italic'
            }
        })

    adding = service.documents().batchUpdate(documentId=docID, body={'requests': formattingList}).execute()
