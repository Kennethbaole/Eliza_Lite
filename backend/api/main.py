from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Eliza_Lite API is running!"}