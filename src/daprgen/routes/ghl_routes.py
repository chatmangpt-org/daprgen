import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger
from daprgen.ghl import GHL, Model, GHL_API_DOMAIN
from httpx import AsyncClient

router = APIRouter()

model = Model()


async def get_client():
    async with AsyncClient(base_url=GHL_API_DOMAIN) as client:
        yield client


async def get_ghl(client: AsyncClient = Depends(get_client)):
    return GHL(model, client)


@router.get("/oauth/callback")
async def oauth_callback(request: Request, ghl: GHL = Depends(get_ghl)):
    code = request.query_params.get('code')
    await ghl.authorization_handler(code)
    return RedirectResponse(url="https://app.gohighlevel.com/")


@router.get("/authorize")
def authorize(request: Request):
    scopes = request.query_params.get('scopes', "conversations.message.readonly conversations.message.write users.readonly")
    scopes_list = scopes.split()
    authorization_url = (
        f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
        f"response_type=code&"
        f"client_id={os.getenv('GHL_APP_CLIENT_ID')}&"
        f"redirect_uri={os.getenv('REDIRECT_URI')}&"
        f"scope={' '.join(scopes_list)}"
    )
    logger.debug(f"Authorization URL: {authorization_url}")
    return RedirectResponse(url=authorization_url)


@router.get("/example-api-call")
async def example_api_call(request: Request, ghl: GHL = Depends(get_ghl)):
    company_id = request.query_params.get('companyId')
    if model.get_access_token(company_id):
        try:
            client = await ghl.requests(company_id)
            response = await client.get(f"/users/search?companyId={company_id}", headers={"Version": "2021-07-28"})
            return JSONResponse(content=response.json())
        except Exception as e:
            logger.error(f"Error in API call: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=500)
    return JSONResponse(content={"error": "Installation for this company does not exist"}, status_code=400)


@router.get("/example-api-call-location")
async def example_api_call_location(request: Request, ghl: GHL = Depends(get_ghl)):
    company_id = request.query_params.get('companyId')
    location_id = request.query_params.get('locationId')
    try:
        if model.get_access_token(location_id):
            client = await ghl.requests(location_id)
            response = await client.get(f"/contacts/?locationId={location_id}", headers={"Version": "2021-07-28"})
            return JSONResponse(content=response.json())
    except Exception as e:
        logger.error(f"Error in API call: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/example-webhook-handler")
async def example_webhook_handler(request: Request):
    payload = await request.json()
    logger.debug(f"Webhook payload: {payload}")
    return JSONResponse(content={"status": "received"})


@router.post("/decrypt-sso")
async def decrypt_sso(request: Request, ghl: GHL = Depends(get_ghl)):
    data = await request.json()
    key = data.get("key")
    if not key:
        return JSONResponse(content={"error": "Please send valid key"}, status_code=400)
    try:
        decrypted_data = await ghl.decrypt_sso_data(key)
        return JSONResponse(content=decrypted_data)
    except Exception as e:
        logger.error(f"Error decrypting SSO data: {e}")
        return JSONResponse(content={"error": "Invalid Key"}, status_code=400)
