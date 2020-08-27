from fastapi import FastAPI

# from routers import wx_api
from user_app import user_app

def creat_app():
    app = FastAPI()
    # app.include_router(wx_api.router)
    app.include_router(user_app.router)
    return app

"""
解决跨域/官方demo姑且放在这儿
from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
