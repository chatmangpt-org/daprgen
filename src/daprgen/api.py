# main.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from daprgen.routes.ghl_routes import router as ghl_router
from ngrok_config import create_ngrok_tunnel, close_ngrok_tunnel

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""

    logger.info("Starting FastAPI application")

    # Start ngrok tunnel with custom domain and port from env
    DOMAIN = os.getenv("DOMAIN")
    PORT = int(os.getenv("PORT", 8000))

    public_url = create_ngrok_tunnel(DOMAIN, PORT)
    logger.info(f"Auth URL: {public_url}/v1/authorize")
    logger.info(f"Callback URL: {public_url}/v1/oauth/callback")
    app.state.public_url = public_url
    logger.info(f"ngrok tunnel set to {public_url}")

    yield

    # Shutdown events
    close_ngrok_tunnel()
    logger.info("Shutting down FastAPI application")


app = FastAPI(lifespan=lifespan)

app.include_router(ghl_router, prefix="/v1")

# http://localhost:8000/v1/oauth/callback

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)