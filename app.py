from fastapi import FastAPI
import chromadb
import ollama
app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
ollama_client = ollama.Client(host="http://localhost:11434")

@app.post("/query")
def query(q: str):
    print(f"Received query: {q}")
    results = collection.query(query_texts=[q], n_results=1)
    print(f"ChromaDB query results: {results}")
    
    context = results["documents"][0][0] if results["documents"] else ""
    print(f"Context passed to Ollama: {context}")

    answer = ollama_client.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:using only the context in the context"
    )
    
    return {"answer": answer["response"]}

@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    try:
        # Generate a unique ID for this document
        import uuid
        doc_id = str(uuid.uuid4())
        
        # Add the text to Chroma collection
        collection.add(documents=[text], ids=[doc_id])
        
        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
