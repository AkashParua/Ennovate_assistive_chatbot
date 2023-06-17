import chromadb
from chromadb.config import Settings
#extracting the manual in text file and storing them as embeddings in vector database 
#!!!RUN THIS SCRIPT ONCE DURING INITIALIZATION OF SERVER to create the embeddings!!!#
def initialize_chromadb(path_to_manual):
    try :
        chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="persist_dir"))
        collection = chroma_client.create_collection(name="manual")
        content = ""
        with open(path_to_manual , 'r') as fl :
            content = fl.read()
        text_chunks = [chunk.strip() for chunk in content.split('##')]
        chunk_ids = [f'e_{i}' for i in range(len(text_chunks))]
        metadatas = [{'source' : 'sample_manual'} for i in range(len(text_chunks))]
        collection.add(
            documents=text_chunks,
            ids=chunk_ids,
            metadatas=metadatas
        )
    except Exception as e :
        print('failed to connect to chroma DB',e)

def delete_collection():
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="persist_dir"))
    chroma_client.delete_collection('manual')

    


initialize_chromadb('sample_manual.txt')
#delete_collection()     #use the function to delete old embeddings in chromaDB by uncommenting it make sure to comment it out while initializing the database 

    
#    
    
        
    