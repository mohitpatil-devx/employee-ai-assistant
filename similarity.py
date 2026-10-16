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


text1 = "Java is a programming language"
text2 = "Python is used for software development"
text3 = "I enjoy eating pizza"

embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)

similarity_12 = cosine_similarity(embedding1, embedding2)
similarity_13 = cosine_similarity(embedding1, embedding3)

print("Similarity: Java and Python:", similarity_12)
print("Similarity: Java and Pizza:", similarity_13)