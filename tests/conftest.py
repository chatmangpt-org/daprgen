import asyncio

import pytest
from dotenv import load_dotenv
from loguru import logger
from pyngrok import ngrok

from daprgen.prototypes.calendar.appointment import SimpleEventPublisher

from daprgen.prototypes.calendar.ghl_calendar_service import GHLCalendarService
from daprgen.prototypes.calendar.repository import InMemoryAppointmentRepository


# Load environment variables from .env file
load_dotenv()


# Mock ngrok for testing purposes
class MockNgrokTunnel:
    def __init__(self, public_url):
        self.public_url = public_url


# Fixture to mock ngrok tunnel creation with function scope
@pytest.fixture(scope="function")
def mock_ngrok_tunnel(monkeypatch):
    def mock_connect(addr, proto=None, name=None, pyngrok_config=None, **options):
        return MockNgrokTunnel("https://chatmangpt.ngrok.dev")

    monkeypatch.setattr(ngrok, "connect", mock_connect)
    logger.info("Mock ngrok tunnel created")
    return MockNgrokTunnel("https://chatmangpt.ngrok.dev")


@pytest.fixture()
def service():
    base_url = "https://stoplight.io/mocks/highlevel/integrations/39582850"
    auth_token = "123"  # Replace with your actual token
    version = "2021-04-15"
    return GHLCalendarService(base_url, auth_token, version)


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def repository():
    return InMemoryAppointmentRepository()


@pytest.fixture
def event_publisher():
    return SimpleEventPublisher()
