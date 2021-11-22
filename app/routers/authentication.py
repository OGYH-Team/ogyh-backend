from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.models.authentication import Login
from app.models.token import Token
from app.models.user import User
from app import database
from app.utils.hashing import Hash
from app.utils.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.oauth2 import get_current_user
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_description="user login in",
    summary="Login in",
    status_code=status.HTTP_201_CREATED,
    # response_model=GetSitesResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": "", "description": "Not found"},
        status.HTTP_201_CREATED: {
            "description": "Log in success",
            "content": {"application/json": {"example": {"response": ""}}},
        },
    },
)
def login(request: OAuth2PasswordRequestForm = Depends()):
    # TODO validate request.username == username in db
    user = ""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
