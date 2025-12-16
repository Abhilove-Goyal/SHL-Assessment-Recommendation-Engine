import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load catalog
df = pd.read_csv("data/processed/shl_catalog.csv")

# Create embedding text
df["embed_text"] = (
    df["name"].fillna("") + ". " +
    df["description"].fillna("")
)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode
embeddings = model.encode(
    df["embed_text"].tolist(),
    show_progress_bar=True,
    normalize_embeddings=True
)

# Build FAISS index
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(np.array(embeddings).astype("float32"))

# Save
faiss.write_index(index, "data/processed/catalog.index")
df.to_csv("data/processed/catalog_meta.csv", index=False)

print("Embeddings built for", len(df), "assessments")