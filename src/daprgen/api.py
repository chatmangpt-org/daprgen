"""daprgen REST API."""

import os
import logging
import importlib
import pkgutil
from pathlib import Path
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import coloredlogs
from fastapi import FastAPI
from loguru import logger

from ngrok_config import create_ngrok_tunnel, close_ngrok_tunnel


# Configure loguru to integrate with standard logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_back and frame.f_globals['__name__'] == __name__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    coloredlogs.install()
    logger.info("Starting FastAPI application")

    # Start ngrok tunnel with custom domain and port from env
    domain = os.getenv("DOMAIN")
    port = int(os.getenv("PORT", 8000))
    public_url = create_ngrok_tunnel(domain, port)
    app.state.public_url = public_url
    logger.info(f"ngrok tunnel set to {public_url}")

    yield

    # Shutdown events
    close_ngrok_tunnel()
    logger.info("Shutting down FastAPI application")


app = FastAPI(lifespan=lifespan)


# Dynamically include all routers from the routes module
def include_all_routers(app: FastAPI, package: str, package_path: Path):
    root = __name__.split(".")[0]
    for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
        module = importlib.import_module(f"{root}.{package}.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)

    # Get the import path of this file withou



# Get the path to the routes directory
routes_path = Path(__file__).parent / "routes"
include_all_routers(app, "routes", routes_path)
