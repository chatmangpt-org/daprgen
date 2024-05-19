from fastapi import APIRouter, Request, Depends
from loguru import logger
from httpx import ASGITransport
from daprgen.api import app
from daprgen.domain.oauth_service import OAuthService
from daprgen.infrastructure.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

router = APIRouter()

# Dependency Injection
def get_oauth_service() -> OAuthService:
    transport = ASGITransport(app=app)
    return OAuthService(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, transport)

@router.get("/oauth/callback/gohighlevel")
async def oauth_callback(request: Request, oauth_service: OAuthService = Depends(get_oauth_service)):
    logger.debug("Received callback request")
    code = request.query_params.get('code')
    if not code:
        logger.error("Authorization code not found in request")
        return {"error": "Authorization code not found"}

    logger.info(f"Authorization code received: {code}")
    try:
        token = await oauth_service.exchange_code_for_token(code)
        logger.info("Access token obtained successfully")
        return token.dict()
    except Exception as e:
        logger.error(f"Error obtaining access token: {e}")
        return {"error": str(e)}
