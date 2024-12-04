import os
from dotenv import load_dotenv

def load_environment_variables():
    """Load environment variables from .env or GitHub Secrets"""
    if not os.getenv("GITHUB_ACTIONS"):
        load_dotenv()
