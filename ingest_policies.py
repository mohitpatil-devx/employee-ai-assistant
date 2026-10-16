"""Load policy sections from employee_policies.txt into ChromaDB."""

import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your local .env file before ingesting policies."
    )

POLICY_FILE = Path(__file__).resolve().parent / "employee_policies.txt"
COLLECTION_NAME = "company_policies"
EMBEDDING_MODEL = "gemini-embedding-001"

if not POLICY_FILE.is_file():
    raise FileNotFoundError(f"Policy file not found: {POLICY_FILE}")

# Each non-empty paragraph becomes one searchable policy section.
policy_sections = [
    section.strip()
    for section in POLICY_FILE.read_text(encoding="utf-8").split("\n\n")
    if section.strip()
]

if not policy_sections:
    raise ValueError(f"No policy sections found in {POLICY_FILE.name}")

gemini_client = genai.Client(api_key=api_key)
chroma_client = chromadb.PersistentClient(path=str(Path(__file__).resolve().parent / "chroma_db"))
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

embeddings = []
for section in policy_sections:
    response = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=section,
    )
    embeddings.append(response.embeddings[0].values)

# Replace the contents so rerunning this script does not leave stale policies.
existing_ids = collection.get().get("ids", [])
if existing_ids:
    collection.delete(ids=existing_ids)

collection.add(
    ids=[f"policy_{index}" for index in range(len(policy_sections))],
    documents=policy_sections,
    embeddings=embeddings,
    metadatas=[{"source": POLICY_FILE.name} for _ in policy_sections],
)

print(f"Ingested {len(policy_sections)} policy sections into ChromaDB.")
