from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = FastAPI()

GHL_CLIENT_ID = os.getenv("GHL_CLIENT_ID")
GHL_CLIENT_SECRET = os.getenv("GHL_CLIENT_SECRET")
DOMAIN = os.getenv("DOMAIN")
PORT = int(os.getenv("PORT", 8000))
REDIRECT_URI = f"https://{DOMAIN}/oauth/callback"

logging.basicConfig(level=logging.DEBUG)

@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get('code')
    async with AsyncClient() as client:
        token_response = await client.post(
            'https://services.leadconnectorhq.com/oauth/token',
            data={
                'client_id': GHL_CLIENT_ID,
                'client_secret': GHL_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
        )
        if token_response.status_code != 200:
            logging.error(f"Token request failed: {token_response.status_code} - {token_response.text}")
            return JSONResponse(content={"error": "Token request failed"}, status_code=token_response.status_code)
        tokens = token_response.json()
        return JSONResponse(content=tokens)

@app.get("/authorize")
def authorize():
    authorization_url = (
        f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
        f"response_type=code&"
        f"client_id={GHL_CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=conversations.message.readonly conversations.message.write"
    )
    logging.debug(f"Authorization URL: {authorization_url}")
    return RedirectResponse(url=authorization_url)

if __name__ == "__main__":
    import uvicorn
    from ngrok_config import create_ngrok_tunnel

    public_url = create_ngrok_tunnel(DOMAIN, PORT)
    logging.info(f"Auth URL: {public_url}/authorize")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
