from fastapi import APIRouter, Depends, HTTPException
from todos.src.database.orm import User
from todos.src.database.repository import UserRepository

from todos.src.schema.request import (
    CreateOTPRequest,
    LogInRequest,
    SignUpRequest,
)
from todos.src.schema.response import JWTResponse, UserSchema
from todos.src.service.user import UserService
from todos.src.cache import redis_client
from todos.src.security import get_access_token

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    hashed_password: str = user_service.hash_password(
        plain_password=request.password
    )
    user: User = User.create(
        username=request.username, hashed_password=hashed_password
    )
    user: User = user_repo.save_user(user=user)  # id = int

    return UserSchema.from_orm(user)


@router.post("/log-in", status_code=200)
def user_log_in_handler(
    request: LogInRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_username(
        username=request.username
    )

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )

    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")

    access_token: str = user_service.create_jwt(
        username=user.username,
    )

    return JWTResponse(access_token=access_token)


@router.post("/email/otp")
def create_otp_handler(
    request: CreateOTPRequest,
    _: str = Depends(get_access_token),
    user_service: UserService = Depends(),
):
    otp: int = user_service.create_otp()
    redis_client.set(request.email, otp)
    redis_client.expire(request.email, 3 * 60)
    return {"otp": otp}


@router.post("/email/otp/verify")
def verify_otp_handler():
    return
