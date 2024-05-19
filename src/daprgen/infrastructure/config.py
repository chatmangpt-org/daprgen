# infrastructure/config.py
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GHL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GHL_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://chatmangpt.ngrok.dev/oauth/callback/gohighlevel")
