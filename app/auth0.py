from jose import jwt, JWTError
import requests
from fastapi import HTTPException

AUTH0_DOMAIN = "SEU-DOMINIO.auth0.com"
API_AUDIENCE = "https://SUA_API_IDENTIFIER"
ALGORITHMS = ["RS256"]

def get_jwks():
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def verify_auth0_token(token: str):
    jwks = get_jwks()
    header = jwt.get_unverified_header(token)
    key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
    if not key:
        raise HTTPException(401, "Invalid token header")
    public_key = {k: key[k] for k in ("kty", "kid", "use", "n", "e")}
    try:
        payload = jwt.decode(token, public_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/")
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid Auth0 token")
