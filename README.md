# Retrieval and Reporting Plugin

## Introduction
This project implements a Chrome extension paired with a FastAPI backend to index and retrieve web pages using embedding-based retrieval. The extension automatically collects page content as you browse and sends it to the backend for semantic indexing. Users can then search for relevant content using natural language queries. This design leverages Retrieval Augmented Generation (RAG) techniques, combining vector embedding, similarity search, and straightforward reporting. Embeddings are computed using Ollama's `nomic-embed-text` model, which generates high-dimensional representations of text for both indexing and query matching.

## Architecture

### Frontend
The frontend is built as a Chrome extension and comprises the following components:
- **Content Script (`content.js`)**  
  Injected into matching pages, it extracts the text content once the DOM is ready and sends it to the background script.
  
- **Background Script (`background.js`)**  
  Acts as a mediator by receiving messages from both the content and popup scripts. It forwards webpage data to the backend for indexing and, for retrieval, forwards query results back to the popup. It also includes a mechanism to open pages and highlight query-related text.
  
- **Popup UI (`popup.html` & `popup.css`)**  
  Provides a simple interface with a search input and a results display, allowing users to enter queries and view matching pages.
  
- **Manifest (`manifest.json`)**  
  Defines the extension's configuration, specifies the scripts to inject, and outlines necessary permissions.

### Backend
The backend is powered by FastAPI and exposes REST endpoints for both indexing and retrieval:
- **Indexing Endpoint (`/index`)**  
  Accepts page data (URL and text) from the extension, computes text embeddings using Ollama's `nomic-embed-text` model (via an external API call), and adds the resulting vectors to an in-memory FAISS index.
  
- **Query Endpoint (`/query`)**  
  Receives user search queries, computes a query embedding using the same `nomic-embed-text` model, and performs a similarity search within the FAISS index to retrieve related pages.
  
- **Reporting Endpoint (`/report/{id}`)**  
  (Optional) Retrieves detailed metadata for a specific page, useful for further reporting.
  
The backend's core components include:
- **`vector_index.py`**: Maintains the FAISS index and an in-memory list of page metadata.
- **`indexing.py` & `retrieval.py`**: Implement the logic for computing embeddings (by calling Ollama's API for the `nomic-embed-text` model), indexing pages, and performing similarity-based retrieval.
- **`utils.py`**: Handles external embedding API calls, specifically configured to use Ollama's `nomic-embed-text` model.

### Database
The project uses an in-memory storage solution:
- **FAISS Index**: An instance of `IndexFlatL2` from FAISS, which performs efficient nearest neighbor searches based on L2 (Euclidean) distance.
- **Page Metadata**: A Python list holds metadata for each page (including URL, text, and timestamp).

> **Note:** For production or larger scale use, consider replacing the in-memory storage with a persistent database solution.

## RAG Implementation

### Indexing
1. **Content Capture:**  
   When a page loads, the content script extracts the text content and notifies the background script.
2. **Backend Indexing:**  
   The background script sends a POST request with the page URL and text to the FastAPI `/index` endpoint.
3. **Embedding Generation:**  
   The FastAPI backend uses Ollama's `nomic-embed-text` model to compute a 768-dimensional embedding for the page text. This is done by calling the external embedding API specified in `utils.py`.
4. **Storage:**  
   The computed embedding is added to the FAISS index, and the page metadata is stored in an in-memory list.

### Retrieval
1. **User Query Input:**  
   Users input search queries via the extension's popup.
2. **Query Processing:**  
   The popup script sends the query to the background script, which then forwards it to the FastAPI `/query` endpoint.
3. **Semantic Matching:**  
   The backend computes an embedding for the query using Ollama's `nomic-embed-text` model and performs a nearest neighbor search on the FAISS index.
4. **Result Display & Highlighting:**  
   Matching pages are sent back to the popup for display. Users can click a result to open the page, where the content script highlights the query text within the page.

## Sample Output

- **Backend Console Logs:**
  ```
  [FastAPI] /index received for URL: https://example.com/page1
  [Indexing] Obtained embedding of shape: (768,)
  [Indexing] Successfully indexed page with FAISS ID: 0
  [FastAPI] /query received for query: "machine learning"
  [Retrieval] Query embedding shape: (768,)
  [Retrieval] Returning 1 results
  ```

- **Chrome Extension Popup UI:**  
  When a user enters a query (e.g., "machine learning"), the popup displays a list of matching pages. Selecting an item opens a new tab for that page with the query text highlighted in yellow.

### Video Demonstration
Check out the following video to see the plugin in action on YouTube:  
[Watch the Demo on YouTube](https://youtu.be/U9h0xbvI6Io)

## Setup and Usage

### Prerequisites
- **Chrome Browser:** For running the extension.
- **Python 3.7+:** To run the FastAPI backend.
- **Dependencies:**  
  Install required Python packages (e.g., FastAPI, uvicorn, faiss, numpy, requests).  
- **Ollama and External Embedding API:**  
  Ensure the external embedding API is running and accessible at `http://localhost:11434/api/embeddings`. This API should be configured to use Ollama's `nomic-embed-text` model for generating embeddings.

### Running the Backend
1. Navigate to the `fastapi_backend` directory:
    ```bash
    cd fastapi_backend
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload --host localhost --port 8000
    ```

### Installing the Chrome Extension
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click on **Load unpacked** and select the directory containing the extension's files.
4. Verify that the Ollama external embedding API and FastAPI backend are running.


