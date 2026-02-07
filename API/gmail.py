import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_authenticate():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


# ✅ AUTHENTICATION
creds = gmail_authenticate()

# ✅ GMAIL CONNECTION
service = build("gmail", "v1", credentials=creds)

print("Login success ✅")


# ===================================================
# 👉 ADD YOUR MAIL OPERATIONS BELOW THIS LINE
# ===================================================

# Example: read latest 5 mails
results = service.users().messages().list(
    userId="me", maxResults=5
).execute()

messages = results.get("messages", [])

print(f"Found {len(messages)} messages")

