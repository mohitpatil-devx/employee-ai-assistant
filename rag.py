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
    "Employees receive 24 paid leaves per year.",
    "Employees must submit leave requests to their manager.",
    "The company provides health insurance to all full-time employees.",
    "Employees should work eight hours per day.",
    "The notice period for employees is 30 days."
]

print("Creating document embeddings...")

document_embeddings = []

for document in documents:
    embedding = get_embedding(document)
    document_embeddings.append(embedding)

question = input("\nAsk a question: ")

question_embedding = get_embedding(question)

results = []

for i in range(len(documents)):
    score = cosine_similarity(
        question_embedding,
        document_embeddings[i]
    )

    results.append((score, documents[i]))

results.sort(reverse=True)

similarity_threshold = 0.60


top_k = 3
similarity_threshold = 0.70

filtered_results = []

for score, document in results:
    if score >= similarity_threshold:
        filtered_results.append((score, document))

filtered_results = filtered_results[:top_k]

context = ""

for score, document in filtered_results:
    context += document + "\n"

if context == "":
    context = "No relevant information was found."

prompt = f"""
You are a helpful company policy assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}

Provide a clear and concise answer.
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("\nRetrieved Context:")
print(context)

print("\nAI Answer:")
print(response.text)