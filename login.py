from fastapi import FastAPI
from pydantic import BaseModel
import jwt
from fastapi.encoders import jsonable_encoder

app = FastAPI()

SECERT_KEY = "YOU_FAST_API_SECRET_KEY"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRES_MINUTES = 800

test_user = {
    "password": "temipassword",
    "email": "temiemail@gmail.com"
}


class LoginItem(BaseModel):
    username: str
    password: str | None = None
    email: str | None = None

    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    


@app.post("/login")
async def user_login(loginitem: LoginItem):

    data = jsonable_encoder(loginitem)

    if data['password'] == test_user['password'] and data['email'] == test_user['email']:

        encoded_jwt = jwt.encode(data, SECERT_KEY, algorithm=ALGORITHM)
        return {"token": encoded_jwt}

    else:
        return {"message": "login failed"}
