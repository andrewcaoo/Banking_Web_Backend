from .api import router
from .core.config import settings
from .core.setup import create_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = create_application(router=router, settings=settings)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}