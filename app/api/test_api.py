from fastapi import APIRouter

test_api = APIRouter()

@test_api.get("/test")
def test():
    return {"message": "Hello, World!"}