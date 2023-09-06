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
            username, self.secret_key, algorithm=self.jwt_algorithm
        )
