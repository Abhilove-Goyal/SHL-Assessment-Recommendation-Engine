🧠 SHL Assessment Recommendation Engine (GenAI + RAG)
=====================================================

A **web-based GenAI-powered Assessment Recommendation System** that recommends the most relevant SHL assessments for a given Job Description (JD), using **semantic retrieval, ranking logic, and LLM-based explanations**.

This project is built as part of the **SHL AI Intern – Generative AI Assignment**.

🚀 Key Features
---------------

*   🔍 **Semantic Retrieval (RAG)** using FAISS + sentence embeddings
    
*   🧠 **GenAI-based Explanation** for why assessments are recommended
    
*   ⚖️ **Custom Re-ranking Logic** (skills, duration, keywords)
    
*   📊 **Automated CSV Submission Format** (as required by SHL)
    
*   🌐 **Deployed Web App** (Streamlit)
    
*   🔌 **API-ready architecture** (FastAPI compatible)
    

🏗️ System Architecture
-----------------------
```
Job Description (Input)
        ↓
Query Enrichment & Cleaning
        ↓
Embedding Generation
        ↓
FAISS Vector Search (Retrieval)
        ↓
Rule-based Re-ranking
        ↓
Top-K Assessment Recommendations
        ↓
GenAI Explanation (LLM)
        ↓
CSV Output & Web UI
```
🧪 Data Sources
---------------

*   **SHL Product Catalog** (crawled from official SHL website)
    
*   **Provided Train & Test Dataset** (Excel → CSV)
    

🧠 Retrieval-Augmented Generation (RAG)
---------------------------------------

### 🔹 Retrieval

*   Sentence embeddings generated using **Sentence Transformers**
    
*   FAISS index built on assessment descriptions
    
*   Top-K relevant assessments retrieved per query
    

### 🔹 Re-ranking

*   Keyword matching (skills, roles)
    
*   Duration-based filtering
    
*   Score boosting for domain alignment
    

### 🔹 Generation (GenAI)

*   LLM generates **natural-language explanations**
    
*   Strict prompt design to:
    
    *   Avoid hallucinations
        
    *   Explain only why selected assessments fit the JD
        
    *   Not suggest unavailable assessments
        

📄 CSV Submission Format (CRITICAL)
-----------------------------------

The system automatically generates output in **exact SHL-required format**:
```
Query,Assessment_URL
Query 1,Recommendation 1 (URL)
Query 1,Recommendation 2 (URL)
Query 1,Recommendation 3 (URL)
.
.
.
Query 2,Recommendation 1 (URL)
```
Users can **download the CSV directly** from the web interface.

🌐 Deployment
-------------

*   **Frontend**: Streamlit Cloud (Free Tier)
    
*   **Backend Logic**: Modular Python (API-ready)
    
*   **LLM**: Free-tier LLM (Groq / Ollama fallback)
    

> ⚠️ Note: On Streamlit free tier, the app may take a few seconds to wake up after inactivity.

🖥️ How to Run Locally
----------------------

### 1️⃣ Clone the repository
```
git clone https://github.com/Abhilove-Goyal/SHL-Assessment-Recommendation-Engine.git  cd SHL-Assessment-Recommendation-Engine
```
### 2️⃣ Install dependencies
```
pip install -r requirements.txt 
```
### 3️⃣ Set environment variables
```
GROQ_API_KEY=your_api_key  API_BASE_URL=http://127.0.0.1:8000  
```
### 4️⃣ Run Streamlit app
```
streamlit run frontend/app.py  
```
📁 Project Structure
--------------------
```
shl-assessment-recommendation-engine/
├── api/                  # FastAPI backend
├── crawler/              # SHL catalog crawler
├── data/
│   ├── raw/              # Original Excel files
│   └── processed/        # Cleaned CSVs + FAISS index
├── embeddings/           # Vector index creation
├── recommender/
│   ├── retrieval.py     # Vector search (RAG retrieval)
│   ├── rerank.py        # Rule-based re-ranking
│   ├── rag_explainer.py # GenAI explanation module
│   └── duration_filter.py
├── evaluation/           # Recall@K evaluation
├── frontend/             # Streamlit web app
├── outputs/              # Submission CSV
├── approach.md           # Detailed methodology
└── README.md
```
📈 Evaluation
-------------

*   **Metric Used**: Recall@10
    
*   **Mean Recall@10**: ~0.50
    
*   Shows effective retrieval despite small catalog size
    

🧩 Design Decisions
-------------------

*   Chose **RAG** over pure LLM to ensure:
    
    *   Deterministic recommendations
        
    *   No hallucinated assessments
        
*   Used **rule-based re-ranking** for explainability
    
*   Kept system **API-compatible** for scalability
    

🔮 Future Improvements
----------------------

*   Add SHAP-style explainability for ranking
    
*   Expand catalog coverage
    
*   Replace rule-based re-ranking with learning-to-rank
    
*   Add authentication & logging
    

📬 Submission Notes
-------------------

*   ✅ Web URL provided
    
*   ✅ CSV format strictly followed
    
*   ✅ GenAI used responsibly
    
*   ✅ Fully reproducible pipeline
    

👤 Author
---------

**Abhilove Goyal**📧 [abhilovegoyal17@gmail.com](mailto:abhilovegoyal17@gmail.com)🔗 [LinkedIn](https://linkedin.com/in/abhilove-goyal)💻 [GitHub](https://github.com/Abhilove-Goyal)
