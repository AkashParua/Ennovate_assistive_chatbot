import chromadb
from chromadb.config import Settings
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="persist_dir"))
collection = client.get_collection("manual")
def query(question , n):
    result = collection.query(
        query_texts= [question],
        n_results=n
    )
    response = [docs for docs in result["documents"][0]]
    return response

