from dotenv import load_dotenv
load_dotenv()
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from pydantic import BaseModel
from recommender.retrieval import retrieve
from recommender.rag_explainer import explain_recommendations

app = FastAPI(title="SHL GenAI Assessment Recommender")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(req: QueryRequest):
    results = retrieve(req.query)

    try:
        explanation = explain_recommendations(req.query, results)
    except Exception as e:
        import traceback
        traceback.print_exc()   # 👈 THIS IS KEY
        explanation = "Explanation could not be generated due to a GenAI error."

    return {
        "query": req.query,
        "recommendations": results,
        "explanation": explanation
    }


