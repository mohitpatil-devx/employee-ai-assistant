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


def split_into_chunks(text, chunk_size=30, overlap=5):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


document = """
Employees receive 24 paid leaves per year. Leave requests must
be submitted to the manager for approval. The company provides
health insurance to all full-time employees. Employees should
work eight hours per day. The notice period is 30 days.
Employees can work remotely with manager approval. Salary
reviews are conducted annually based on performance.
"""

chunks = split_into_chunks(document)

print("Creating chunk embeddings...")

chunk_embeddings = []

for chunk in chunks:
    embedding = get_embedding(chunk)
    chunk_embeddings.append(embedding)


question = input("\nAsk a question: ")

question_embedding = get_embedding(question)

results = []

for i in range(len(chunks)):
    score = cosine_similarity(
        question_embedding,
        chunk_embeddings[i]
    )

    results.append((score, chunks[i]))

results.sort(reverse=True)

top_k = 2
similarity_threshold = 0.60

context = ""

for score, chunk in results[:top_k]:
    if score >= similarity_threshold:
        context += chunk + "\n"

if context == "":
    context = "No relevant information was found."


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