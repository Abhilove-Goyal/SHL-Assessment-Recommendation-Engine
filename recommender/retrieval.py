import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from recommender.query_enrichment import enrich_query
from recommender.rerank import rerank

# Load index + metadata
index = faiss.read_index("data/processed/catalog.index")
meta = pd.read_csv("data/processed/catalog_meta.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, top_k=10):
    # 1. Enrich query
    enriched_query = enrich_query(query)

    # 2. Encode query
    q_emb = model.encode([enriched_query], normalize_embeddings=True)

    # 3. Vector search (get more than needed for reranking)
    scores, idxs = index.search(
        np.array(q_emb).astype("float32"),
        top_k * 2
    )

    # 4. Build results with scores
    results = meta.iloc[idxs[0]].assign(
        score=scores[0]
    ).to_dict(orient="records")

    # 5. Re-rank using heuristics
    results = rerank(results, query)

    # 6. Return top_k
    return results[:top_k]
