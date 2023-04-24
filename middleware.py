from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # 指示跨域请求支持 cookies。默认是 False
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)


@app.get('/')
async def main():
    return {"message": "hello world"}