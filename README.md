Document Retrieval System Backend

This repository contains the backend for a document retrieval system designed to provide context for chat applications leveraging Large Language Models (LLMs).

Features:
Document Retrieval System: Efficient backend for retrieving documents stored in a database. Cached responses ensure faster retrieval and enhance overall system performance.
Background Task: When the server starts, a separate thread initiates to continuously scrape and store news articles.
Dockerized Application: The backend is containerized using Docker for easy deployment and scalability.
Rate Limiting: Limits users to a maximum of 5 requests before returning an HTTP 429 error. Additionally, logs each API request and tracks the response time.
Endpoints:
/health: Confirms that the API is active and running.
/search: Returns the top search results based on query parameters like text, top_k, and threshold.
