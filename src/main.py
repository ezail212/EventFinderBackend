import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers.Authentication import router as AuthRouter
from routers.Events import router as TestRouter
from fastapi.middleware.cors import CORSMiddleware

# Basic FastAPI Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Event Finder",
    version="1.0.0",
    docs_url="/",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(TestRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=False)