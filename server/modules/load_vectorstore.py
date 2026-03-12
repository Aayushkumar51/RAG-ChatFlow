import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = Path(__file__).resolve().parents[1]  # points to `server/`
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
# Use a dedicated index name for 3072-dim embeddings
PINECONE_INDEX_NAME = "medicalindex-3072"

if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ.setdefault("PINECONE_INDEX_NAME", PINECONE_INDEX_NAME)


UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _get_pinecone_index():
    """
    Lazily initialize Pinecone so the app can start
    even if PINECONE_API_KEY is missing. We only error
    when vectorstore operations are actually used.
    """
    if not PINECONE_API_KEY:
        raise RuntimeError(
            "PINECONE_API_KEY is not set. Please add it to your .env file."
        )

    pc = Pinecone(api_key=PINECONE_API_KEY)
    spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    existing_indexes = [i["name"] for i in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            # gemini-embedding-001 currently returns 3072-dim vectors
            dimension=3072,
            metric="dotproduct",
            spec=spec,
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            time.sleep(1)

    return pc.Index(PINECONE_INDEX_NAME)


# load, split, embed and upsert pdf docs content

def load_vectorstore(uploaded_files):
    # gemini-embedding-001 has 768-dim vectors, matching the Pinecone index
    embed_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {**chunk.metadata, "text": chunk.page_content}
            for chunk in chunks
        ]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"🔍 Embedding {len(texts)} chunks...")
        embeddings = embed_model.embed_documents(texts)

        print("📤 Uploading to Pinecone...")
        index = _get_pinecone_index()
        vectors = [
            {"id": i, "values": e, "metadata": m}
            for i, e, m in zip(ids, embeddings, metadatas)
        ]
        with tqdm(total=len(vectors), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=vectors)
            progress.update(len(vectors))

        print(f"✅ Upload complete for {file_path}")