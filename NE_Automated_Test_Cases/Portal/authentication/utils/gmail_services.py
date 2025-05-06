import os.path
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
import re
from requests import Request
from urllib.parse import unquote
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API using OAuth2"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_latest_reset_email(service, max_retries=3, retry_delay=5):
    """
    Fetches the most recent password reset email with retry logic.
    
    Args:
        service: Authenticated Gmail service
        max_retries: Number of times to retry fetching the email
        retry_delay: Seconds to wait between retries
        
    Returns:
        The reset link or None if not found
    """
    for attempt in range(max_retries):
        try:
            # More specific query to find reset emails
            query = 'subject:(reset OR "password reset" OR "reset password")'
            results = service.users().messages().list(
                userId='me', 
                labelIds=['INBOX'], 
                q=query,
                maxResults=1
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                print("No password reset emails found.")
                return None
            
            # Get the most recent message
            message = service.users().messages().get(
                userId='me', 
                id=messages[0]['id'],
                format='full'
            ).execute()
            
            return extract_reset_link_from_message(message)
            
        except HttpError as error:
            print(f"Attempt {attempt + 1} failed: {error}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None

def extract_reset_link_from_message(message):
    """Extracts the reset link from an email message"""
    payload = message['payload']
    parts = payload.get('parts', [payload])  # Handle both multipart and singlepart
    
    for part in parts:
        mime_type = part.get('mimeType', '')
        body_data = part.get('body', {}).get('data', '')
        
        if mime_type == 'text/html' and body_data:
            try:
                html = base64.urlsafe_b64decode(body_data).decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                
                # More robust link finding approaches:
                
                # 1. First try: Look for anchor with reset text (handles nested spans)
                reset_anchors = soup.find_all('a')
                for anchor in reset_anchors:
                    if 'reset' in anchor.get_text().lower():
                        href = anchor.get('href', '')
                        if href and 'http' in href:
                            return unquote(href)  # Decode URL-encoded characters
                
                # 2. Second try: Look for common reset link patterns
                possible_links = soup.find_all('a', href=True)
                for link in possible_links:
                    href = link['href']
                    if any(keyword in href.lower() for keyword in ['reset', 'password', 'token']):
                        return unquote(href)
                
                # 3. Fallback: Search entire HTML for URLs containing reset tokens
                url_pattern = re.compile(r'https?://[^\s<>"\']+reset[^\s<>"\']*')
                found_urls = url_pattern.findall(html)
                if found_urls:
                    return unquote(found_urls[0])
                
            except Exception as e:
                print(f"Error parsing email content: {e}")
                continue
    
    print("No reset link found in email.")
    return None