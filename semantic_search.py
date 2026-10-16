import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def cosine_similarity(vector_a, vector_b):
    dot_product = 0
    magnitude_a = 0
    magnitude_b = 0

    for i in range(len(vector_a)):
        dot_product += vector_a[i] * vector_b[i]
        magnitude_a += vector_a[i] ** 2
        magnitude_b += vector_b[i] ** 2

    return dot_product / (
        math.sqrt(magnitude_a) * math.sqrt(magnitude_b)
    )


documents = [
    "Java is an object-oriented programming language.",
    "Python is commonly used in artificial intelligence.",
    "SQL is used to manage and query databases.",
    "Regular exercise improves physical fitness.",
    "Machine learning models learn patterns from data."
]

print("Creating document embeddings...")

document_embeddings = []

for document in documents:
    embedding = get_embedding(document)
    document_embeddings.append(embedding)

query = input("\nEnter your search query: ")

query_embedding = get_embedding(query)

results = []

for i in range(len(documents)):
    score = cosine_similarity(
        query_embedding,
        document_embeddings[i]
    )

    results.append((score, documents[i]))

results.sort(reverse=True)

top_results = results[:3]

print("\nTop 3 Search Results:")

for score, document in top_results:
    print(f"{score:.4f} - {document}")