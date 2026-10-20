# app.py
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# This is what the API *should* receive
class UserRequest(BaseModel):
    user_id: int
    email: str

@app.post("/users")
async def create_user(user: UserRequest):
    # 🚩 INTENTIONAL BUG: Returning "id" as a string ("999") instead of an integer (999)
    # This directly violates our Swagger contract!
    return {
        "status": "success",
        "id": "999" 
    }

if __name__ == "__main__":
    import uvicorn
    # Start the server on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
