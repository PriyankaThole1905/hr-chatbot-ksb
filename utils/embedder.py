from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_embedder():
    return SentenceTransformerEmbeddings("all-MiniLM-L6-v2")
