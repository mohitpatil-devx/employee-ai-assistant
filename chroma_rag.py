import os
import chromadb

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="company_policies"
)


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


documents = [
    "Employees receive 24 paid leaves per year.",
    "Leave requests must be submitted to the manager for approval.",
    "The company provides health insurance to all full-time employees.",
    "Employees should work eight hours per day.",
    "The notice period is 30 days.",
    "Employees can work remotely with manager approval.",
    "Salary reviews are conducted annually based on performance."
]

categories = [
    "leave",
    "leave",
    "benefits",
    "work",
    "notice",
    "remote_work",
    "salary"
]


# Add documents only if collection is empty
if collection.count() == 0:
    print("Adding documents to ChromaDB...")

    embeddings = []

    for document in documents:
        embeddings.append(get_embedding(document))

    collection.add(
    ids=[f"doc_{i}" for i in range(len(documents))],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"category": categories[i]}
        for i in range(len(documents))
    ]
)

    print("Documents added successfully.")

else:
    print("Documents already exist in ChromaDB.")


question = input("\nAsk a question: ")

query_embedding = get_embedding(question)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

retrieved_documents = results["documents"][0]

context = "\n".join(retrieved_documents)


prompt = f"""
You are a company policy assistant.

Answer only using the provided context.

If the answer is unavailable, say:
"I do not have enough information."

Context:
{context}

Question:
{question}

Give a concise and accurate answer.
"""


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("\nRetrieved Context:")
print(context)

print("\nAI Answer:")
print(response.text)