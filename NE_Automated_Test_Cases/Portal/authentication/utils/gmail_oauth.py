from email.mime.text import MIMEText
import os
import pickle
import time
import base64
import logging

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# Only use the readonly scope since we only need to read reset password emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Get the directory where this script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_gmail_service():
    creds = None
    token_path = os.path.join(CURRENT_DIR, 'token.pickle')
    credentials_path = os.path.join(CURRENT_DIR, 'credentials.json')
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_inbox(service):
    """Get inbox messages from the Gmail account."""
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print('No new messages.')
        else:
            print('New messages:')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name == 'From':
                        from_name = values['value']
                        print(f'From: {from_name}')

                print(f'Message snippet: {msg["snippet"]}\n')

    except HttpError as error:
        print(f'An error occurred: {error}')

def send_email(service, to, subject, body):
    """Send an email using Gmail API."""
    try:
        message = create_message('me', to, subject, body)
        send_message(service, 'me', message)
    except HttpError as error:
        print(f'An error occurred: {error}')

def create_message(sender, to, subject, body):
    """Create a message for an email."""
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}

def send_message(service, sender, message):
    """Send the message via the Gmail API."""
    try:
        message = service.users().messages().send(userId=sender, body=message).execute()
        print(f'Sent message to {sender} Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == '__main__':
    # Authenticate and access Gmail API
    service = get_gmail_service()

    # Get inbox messages (example of reading inbox)
    if service:
        get_inbox(service)

    # Example of sending an email (comment this out if you don't want to send a test email)
    # send_email(service, 'recipient_email@example.com', 'Test Subject', 'This is a test email.')
