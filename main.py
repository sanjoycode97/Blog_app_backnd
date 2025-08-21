import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from database import models  # noqa
from routers import post

load_dotenv()

# Auto-create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0")

# CORS
origins_raw = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = ["*"] if origins_raw == "*" else [o.strip() for o in origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(post.router)

@app.get("/")
def root():
    return {"status": "ok"}
