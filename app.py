```python
import openai
import faiss
import os
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key securely

# Sample permit sections
with open("sample_permit.txt", "r") as f:
    raw_text = f.read()

# Simulated chunking
chunks = [raw_text[i:i+500] for i in range(0, len(raw_text), 500)]

# Embed chunks
def embed_chunks(chunks: List[str]):
    return [openai.Embedding.create(input=chunk, model="text-embedding-ada-002")['data'][0]['embedding'] for chunk in chunks]

# Build FAISS index
vectors = embed_chunks(chunks)
d = len(vectors[0])
index = faiss.IndexFlatL2(d)
index.add(np.array(vectors).astype('float32'))

# RAG prompt
query = "Extract key permit details: applicant name, project address, scope of work, approval date."
query_vector = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']
D, I = index.search(np.array([query_vector]).astype('float32'), k=3)

relevant_chunks = [chunks[i] for i in I[0]]
context = "\n".join(relevant_chunks)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a document assistant trained to extract structured data."},
        {"role": "user", "content": f"{context}\n\nPlease extract the applicant name, project address, scope of work, and approval date."}
    ]
)

print(response['choices'][0]['message']['content'])
```

---
