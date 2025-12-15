import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter/LLM Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
LLM_MODEL_NAME = "google/gemma-3-12b-it:free" # As requested

# Blogger Configuration
BLOG_ID = os.getenv("BLOG_ID")
CLIENT_SECRET_PATH = os.getenv("CLIENT_SECRET_PATH", 'client_secret.json') # Path to the client secret file
API_NAME = 'blogger'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/blogger']

# News and Trend Configuration
GNEWS_MAX_RESULTS = 5
PYTRENDS_HL = 'ko-KR' # Host Language
PYTRENDS_GEO = 'KR' # Geo location for trends

# Application settings
DEFAULT_LANGUAGE = 'Korean'

class ConfigError(Exception):
    pass

def validate_config():
    """Validates that all necessary configuration variables are set."""
    if not OPENROUTER_API_KEY:
        raise ConfigError("OPENROUTER_API_KEY is not set in the .env file.")
    if not BLOG_ID or BLOG_ID == "YOUR_BLOG_ID":
        raise ConfigError("BLOG_ID is not set or is still the default value in the .env file.")
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise ConfigError(
            f"Client secret file not found at '{CLIENT_SECRET_PATH}'.\n"
            "Please make sure the file exists or set the correct path "
            "using the CLIENT_SECRET_PATH environment variable in your .env file."
        )

# You can add a call to validate_config() here if you want to fail early
# e.g., validate_config()
