import os
import json
from typing import List
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

from utils.pdf_parser import load_all_pdfs

# === Paths ===
VECTOR_DIR = "vector_store/faiss_index"
INDEX_FILE = os.path.join(VECTOR_DIR, "index.faiss")
METADATA_FILE = "vector_store/file_times.json"
PDF_DIR = "docs"
PDF_PATHS = [
    "docs/PDFContent.pdf",
    "docs/SERVICE MILESTONE RECOGNITION POLICY_R1.pdf"
]

# === Auto Reload Vector Store Logic ===
def should_update_index(pdf_paths: List[str]) -> bool:
    if not os.path.exists(METADATA_FILE):
        return True
    try:
        with open(METADATA_FILE, "r") as f:
            old_times = json.load(f)
    except Exception:
        return True

    for path in pdf_paths:
        fname = os.path.basename(path)
        current_time = os.path.getmtime(path)
        if fname not in old_times or current_time != old_times[fname]:
            return True
    return False

def create_vector_index(pdf_paths):
    documents = load_all_pdfs()

    if not documents:
        raise ValueError("No documents found. Please check your 'docs/' folder.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("❌ No text chunks were created from the documents.")

    # ✅ Diagnostic: See how many chunks each file generated
    from collections import defaultdict
    source_chunk_counts = defaultdict(int)
    for doc in chunks:
        source_chunk_counts[doc.metadata.get("source", "unknown")] += 1
    print("\n📊 Chunk count by file:")
    for fname, count in source_chunk_counts.items():
        print(f"- {fname}: {count} chunks")

    print(f"[✅] Total chunks: {len(chunks)}")

    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedder)
    db.save_local(VECTOR_DIR)

    file_times = {os.path.basename(f): os.path.getmtime(f) for f in pdf_paths}
    with open(METADATA_FILE, "w") as f:
        json.dump(file_times, f)


def load_vector_store():
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(VECTOR_DIR, embedder, allow_dangerous_deserialization=True)

# === 🔥 Main Response Function ===
def generate_response(query):
    if should_update_index(PDF_PATHS):
        docs = load_all_pdfs()
        print(f"[📄] Loading PDFs — Total Documents: {len(docs)}")
        for doc in docs[:3]:
            print("🔹 Preview:", doc.page_content[:100])
        create_vector_index(PDF_PATHS)

    db = load_vector_store()
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = Ollama(model="mistral")  # or "llama3", etc.

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa({"query": query})
    answer = result["result"]



    return answer.strip() 
