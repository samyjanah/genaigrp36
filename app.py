import os
import streamlit as st
from PyPDF2 import PdfReader
import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

# Initialisation modèles
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
generator = pipeline("text-generation", model="distilgpt2", max_new_tokens=100)

# Découpage par phrase
def split_text_to_chunks(text):
    sentences = re.split(r'\.\s+|\n+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 30]

# Extraction + découpage
def load_documents(path="./docs"):
    corpus = []
    sources = []
    for filename in os.listdir(path):
        if filename.endswith(".pdf"):
            reader = PdfReader(open(os.path.join(path, filename), "rb"))
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    chunks = split_text_to_chunks(text)
                    corpus.extend(chunks)
                    sources.extend([f"{filename} - page {i+1}"] * len(chunks))
    return corpus, sources

# Indexation FAISS
def create_faiss_index(corpus):
    embeddings = embedder.encode(corpus)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index

# Recherche du top 1
def get_best_chunk(query, corpus, index):
    query_vec = embedder.encode([query])
    D, I = index.search(query_vec, 1)
    return corpus[I[0][0]], I[0][0]

# Interface utilisateur
st.title("Assistant RH 🔍 - Groupe 36")
question = st.text_input("Posez votre question ici 👇")

if question:
    with st.spinner("Recherche dans les documents..."):
        corpus, sources = load_documents()
        index = create_faiss_index(corpus)
        best_chunk, idx = get_best_chunk(question, corpus, index)

        prompt = f"Voici un extrait d’un document RH :\n{best_chunk}\n\nRéponds à cette question : {question}"
        response = generator(prompt, num_return_sequences=1)[0]['generated_text']

        st.subheader("💬 Réponse générée :")
        st.write(response)

        st.caption(f"📄 Source : {sources[idx]}")
