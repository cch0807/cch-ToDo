import random
from datetime import datetime, timedelta
import time
import bcrypt
from jose import jwt


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = (
        "65d93023517c093186470fc1cd8d18d8bf7f512038c4c4656fb9213cd1e1e725"
    )
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {"sub": username, "exp": datetime.now() + timedelta(days=1)},
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # TODO: need token expire
        return payload["sub"]

    @staticmethod
    def create_otp() -> int:
        return random.randint(1000, 9999)

    @staticmethod
    def send_email_to_user(email: str) -> None:
        time.sleep(3)
        print(f"Sending email to {email}")
