import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routes import ai_scraper, user
from api.db.mongodb import close_mongo_connection, connect_to_mongo


load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI()


# Allow localhost during development, and your specific frontend URL in production
if ENVIRONMENT == "development":
    origins = [
        "http://localhost",
        "http://localhost:8000",  # if you're using a specific port
        "http://localhost:5173",
        "http://127.0.0.1",  # another common localhost address
    ]
else:
    origins = ["https://your-frontend-url.com"]  # Replace with the actual frontend URL

# CORS middleware to restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["user"])
app.include_router(ai_scraper.router, prefix="", tags=["scraper"])


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
