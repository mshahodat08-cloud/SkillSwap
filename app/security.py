
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN")
bearer_scheme = HTTPBearer(auto_error=False)


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
):
    if not ADMIN_API_TOKEN:
        raise RuntimeError("ADMIN_API_TOKEN sozlanmagan")

    if credentials is None or not secrets.compare_digest(
        credentials.credentials,
        ADMIN_API_TOKEN,
    ):
        raise HTTPException(
            status_code=401,
            detail="Autentifikatsiya talab qilinadi",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
