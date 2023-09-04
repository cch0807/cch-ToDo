from fastapi import APIRouter, Depends
from todos.src.database.orm import User
from todos.src.database.repository import UserRepository

from todos.src.schema.request import SignUpRequest
from todos.src.schema.response import UserSchema
from todos.src.service.user import UserService

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
