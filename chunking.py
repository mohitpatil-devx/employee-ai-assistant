def split_into_chunks(text, chunk_size=20, overlap=5):
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
"""

chunks = split_into_chunks(document)

for i in range(len(chunks)):
    print(f"\nChunk {i + 1}:")
    print(chunks[i])