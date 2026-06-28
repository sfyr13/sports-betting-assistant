import chromadb
from app.config import settings

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION_NAME
)

def add_documents(documents: list[str], ids: list[str], metadatas: list[dict] = None):
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas or []
    )

def query_documents(query_text: str, n_results: int = 5):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"][0] if results["documents"] else []