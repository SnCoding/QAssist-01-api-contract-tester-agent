from fastapi import FastAPI

app = FastAPI(title="API Contract Tester Agent")

@app.get("/")
def read_root():
    return {"message": "Welcome to your API Contract Tester Agent!"}
