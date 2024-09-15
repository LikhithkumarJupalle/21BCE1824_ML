from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import time
import psycopg2

app = FastAPI()

# Initialize Redis for caching
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="localhost",
    database="document_db",
    user="myuser",
    password="mypassword"
)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "Service is up and running"}

# Request body model for search
class SearchRequest(BaseModel):
    text: str
    top_k: int = 5
    threshold: float = 0.5
    user_id: int

# Function to insert a new document into the database
def store_document(content: str):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO documents (content) VALUES (%s) RETURNING id;", (content,))
        document_id = cursor.fetchone()[0]
        conn.commit()
    return document_id

# Function to retrieve similar documents from the database
def fetch_similar_documents(query: str, top_k: int, threshold: float):
    with conn.cursor() as cursor:
        cursor.execute("SELECT content FROM documents;")
        docs = cursor.fetchall()
    
    # Here, similarity scoring with embeddings would take place
    return [{"doc": doc[0], "score": 0.9} for doc in docs][:top_k]

# Function to cache search results
def cache_results(user_id: int, results: list):
    cache.set(f"search:{user_id}", str(results), ex=3600)

# Function to check if cached results exist
def retrieve_cached_results(user_id: int):
    cached = cache.get(f"search:{user_id}")
    if cached:
        return eval(cached)  # Convert cached string back to list
    return None

# Search endpoint with caching and rate limiting
@app.post("/search")
def search(req: SearchRequest):
    start_time = time.time()

    # Check if the user has exceeded the request limit
    user_key = f"user:{req.user_id}:requests"
    user_requests = cache.get(user_key)

    if user_requests and int(user_requests) >= 5:
        raise HTTPException(status_code=429, detail="Request limit exceeded")

    # Check cache for previous results
    cached_results = retrieve_cached_results(req.user_id)
    if cached_results:
        return {"results": cached_results, "cached": True}

    # Perform search if no cache found
    search_results = fetch_similar_documents(req.text, req.top_k, req.threshold)

    # Cache the new search results
    cache_results(req.user_id, search_results)

    # Increment user request count and set expiration
    cache.incr(user_key)
    cache.expire(user_key, 3600)  # Reset the count every hour

    inference_time = time.time() - start_time

    return {
        "results": search_results,
        "inference_time": inference_time,
        "cached": False
    }
