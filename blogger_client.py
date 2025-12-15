import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import BLOG_ID, CLIENT_SECRET_PATH, API_NAME, API_VERSION, SCOPES, ConfigError

TOKEN_PICKLE_FILE = 'token.pickle'

def get_blogger_service():
    """
    Authenticates with the Blogger API and returns a service object.
    Handles the OAuth 2.0 flow and token management.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing API token...")
            creds.refresh(Request())
        else:
            print("No valid credentials found. Starting authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print(f"Credentials saved to '{TOKEN_PICKLE_FILE}'")

    try:
        print("Blogger API service created successfully.")
        service = build(API_NAME, API_VERSION, credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred while creating the Blogger service: {e}")
        return None


def create_post(service, title: str, content: str, is_draft: bool = True) -> dict | None:
    """
    Creates a new post on the blog.

    Args:
        service: The authenticated Blogger API service object.
        title (str): The title of the post.
        content (str): The HTML content of the post.
        is_draft (bool): Whether to create the post as a draft.

    Returns:
        The created post resource dictionary, or None on failure.
    """
    try:
        if not BLOG_ID:
            raise ConfigError("BLOG_ID is not set. Please check your .env file.")

        print(f"Creating post with title: '{title}'...")
        posts = service.posts()
        body = {
            "title": title,
            "content": content
        }
        # The insert method creates a new post.
        # If isDraft is True, the post is saved as a draft. Otherwise, it's published.
        post = posts.insert(blogId=BLOG_ID, body=body, isDraft=is_draft).execute()
        
        status = "Draft" if is_draft else "Published"
        print(f"Post created successfully as a {status}. URL: {post['url']}")
        return post

    except Exception as e:
        print(f"An error occurred while creating the post: {e}")
        return None
