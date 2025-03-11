from api import comments
from fastapi import FastAPI

app = FastAPI(title="Only Comments Microservice")

app.include_router(comments.router, prefix="/comments", tags=["comments"])
