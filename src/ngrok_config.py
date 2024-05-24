# ngrok_config.py
import os
from pyngrok import ngrok
from loguru import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_ngrok_tunnel(domain: str, port: int) -> str:
    options = {"addr": port}
    if domain:
        options["hostname"] = domain

    try:
        ngrok.kill()
        tunnel = ngrok.connect(**options)
        public_url = tunnel.public_url
        logger.info(f"ngrok tunnel opened at {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Failed to open ngrok tunnel: {e}")
        raise

def close_ngrok_tunnel():
    try:
        ngrok.kill()
        logger.info("ngrok tunnel closed")
    except Exception as e:
        logger.error(f"Failed to close ngrok tunnel: {e}")

# Usage
if __name__ == "__main__":
    domain = os.getenv("DOMAIN")
    port = int(os.getenv("PORT", 8000))
    create_ngrok_tunnel(domain, port)
