from fastapi import FastAPI
from app.api.test_api import test_api
from app.core.db import Base, engine
from app.models import user  # Import all your models
from app.api.auth import auth_api

app = FastAPI()



# This will create all tables that do not yet exist
Base.metadata.create_all(bind=engine)
print("All tables created!")

app.include_router(test_api, prefix="/api", tags=["test"])
app.include_router(auth_api, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}