from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from starlette.routing import request_response
from app.models.authentication import LoginResponse
from app.models.basic_model import Message
from app.models.token import Token
from app.models.user import User
from app.database import retrieve_user, retrieve_password
from app.utils.hashing import Hash
from app.utils.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.oauth2 import get_current_user
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["authentication"])


@router.post(
    "/login",
    response_description="user login in",
    summary="Login in",
    status_code=status.HTTP_201_CREATED,
    response_model=LoginResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message, "detail": "Not found"},
    },
)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    """
    ## Loggin users in the API:
    - **username** : your valid username.
    - **password** : your valid password.

    Keys in the request body are auto-generated from **OAuth2PasswordRequestForm**.
    """   
    user = await retrieve_user(request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    password = user["password"]
    if not Hash.verify(password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": password}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    ## Show a current user
    """
    user = await retrieve_password(current_user.username)
    return user
