import os
from pathlib import Path

from dotenv import load_dotenv

# import pytz

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(env_path)

# MYSQL_URL = os.environ
MONGODB_URL = os.getenv("MONGODB_URL")
MYSQL_URL = os.getenv("MYSQL_URL")
print(MYSQL_URL)

# # misc
# # TIMEZONE = pytz.timezone("Asia/Seoul")

# # 토큰 관련
# # to get a string like this run:  openssl rand -hex 32
# JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
# JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]
# ALGORITHM = "HS256"

# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30분
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1주일
