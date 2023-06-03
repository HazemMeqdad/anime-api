import fastapi
from application import WitClient
from database import Database
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = fastapi.FastAPI(
    debug=True,
    title="Anime API",
    description="An API for anime"
)
db = Database(os.getenv("MONGODB_URL"))
wit = WitClient(db)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/anime/{name:str}")
def anime(name: str):
    search_results = wit.search_anime(name)
    if not search_results:
        return {"error": "Anime not found"}, 404
    return search_results

@app.get("/anime/{name:str}/{index:int}")
def anime(name: str, index: int):
    search_results = wit.search_anime(name)
    if not search_results:
        return {"error": "Anime not found"}, 404
    return search_results[index]

@app.get("/anime/{name:str}/{index:int}/episodes")
def episodes(name: str, index: int):
    search_results = wit.search_anime(name)
    if not search_results:
        return {"error": "Anime not found"}, 404
    res = wit.get_espiodes(search_results[index]["page"])
    return res

@app.get("/anime/{name:str}/{index:int}/episodes/{episode:int}")
def episodes(name: str, index: int, episode: int):
    search_results = wit.search_anime(name)
    if not search_results:
        return {"error": "Anime not found"}, 404
    page_watch = wit.get_espiodes(search_results[index]["page"])
    res = wit.get_servers(page_watch[episode]["watch_page"])
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

