import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="company_policies"
)


def get_embedding(text: str):
    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def search_company_policy(question: str) -> str:
    """Search company policy documents for relevant information."""

    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant company policy found."

    return "\n".join(documents)