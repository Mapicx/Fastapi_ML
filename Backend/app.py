# main/main.py (correct imports)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import predict  # Absolute import
from Backend.database import engine, SessionLocal, Base  # Import actual names
from Backend.config import settings

# Initialize tables (if needed)
Base.metadata.create_all(bind=engine) # type: ignore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)


@app.get("/")
def root():
    return {"message": "API is working!"}