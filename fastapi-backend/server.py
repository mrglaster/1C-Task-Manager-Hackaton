import atexit
import json
import os

import uvicorn
from fastapi import FastAPI, Request

from modules.database.database_operations import create_connection, process_registration, process_authorisation, \
    get_data, upload_data

app = FastAPI()
DATABASE_PATH = "./db/database/database.db"
CONNECTION = create_connection(DATABASE_PATH)


@app.post("/user/register")
async def register_user(info: Request):
    """Function Processing Register Request
    main parameters:
        :param login - login of the user
        :param password - password of the user
    """
    req_info = await info.json()
    login = req_info["login"]
    password = req_info["password"]
    return process_registration(CONNECTION, login, password)


@app.post("/user/auth")
async def auth_user(info: Request):
    req_info = await info.json()
    login = req_info["login"]
    password = req_info["password"]
    return process_authorisation(CONNECTION, login, password)


@app.post("/data/synch/download")
async def download_data(info: Request):
    req_info = await info.json()
    token = str(req_info["token"])
    return get_data(CONNECTION, token)


@app.post("/data/synch/upload")
async def upload_data_request(info: Request):
    req_info = await info.json()
    token = req_info["token"]
    return upload_data(CONNECTION, str(token), str(req_info["data"]))


def on_exit():
    """Saves database on exit"""
    print("Saving Database...")
    CONNECTION.commit()
    print("Saved!")


def main():
    atexit.register(on_exit)
    uvicorn.run(f"{os.path.basename(__file__)[:-3]}:app", log_level="info")


if __name__ == "__main__":
    """Invokes the main function, starts the server"""
    main()
