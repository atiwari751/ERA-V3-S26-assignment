from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from indexing import index_page
from retrieval import query_pages
from vector_index import page_metadata

app = FastAPI()

class PageContent(BaseModel):
    url: str
    text: str

class QueryRequest(BaseModel):
    query: str

@app.post("/index")
async def index_endpoint(page: PageContent):
    """
    Endpoint to index a web page.
    Receives a URL & text, computes its embedding, and adds it to the FAISS index.
    """
    print(f"[FastAPI] /index received for URL: {page.url}")
    idx = await index_page(page.url, page.text)
    print(f"[FastAPI] Indexed page with id: {idx}")
    return {"status": "success", "id": idx}

@app.post("/query")
async def query_endpoint(q: QueryRequest):
    """
    Endpoint to retrieve pages.
    Given a query string, computes its embedding and returns the top matching pages.
    """
    print(f"[FastAPI] /query received for query: {q.query}")
    results = await query_pages(q.query)
    print(f"[FastAPI] Query results: {results}")
    return {"results": results}

@app.get("/report/{id}")
async def report_endpoint(id: int):
    """
    (Optional) Return detailed metadata for a specific indexed page.
    """
    if id < 0 or id >= len(page_metadata):
        raise HTTPException(status_code=404, detail="Page not found")
    return page_metadata[id]

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
