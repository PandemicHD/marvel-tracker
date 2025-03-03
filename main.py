from fastapi import FastAPI
import uvicorn
from scraper import get_rank  # Import Selenium function

app = FastAPI()

@app.get("/get_rank/{username}")
async def get_player_rank(username: str):
    result = get_rank(username)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
