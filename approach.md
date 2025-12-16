Approach: GenAI-Based Assessment Recommendation Engine
======================================================

1\. Problem Understanding
-------------------------

The objective of this project is to build a **web-based GenAI-powered assessment recommendation engine** that recommends suitable SHL assessments based on a natural language job description or hiring query. The system must return **5–10 relevant individual assessments**, exclude pre-packaged job solutions, and provide a clear justification for each recommendation. Additionally, the solution must be evaluated using **Recall@K** and produce outputs in a **strict CSV format** for automated evaluation.

2\. Data Collection & Preparation
---------------------------------

### 2.1 SHL Product Catalog Extraction

To ensure recommendations are grounded in real SHL offerings, an automated **web crawling pipeline** was implemented to extract assessment metadata from the SHL product catalog.

*   Crawling logic handles pagination and individual product pages
    
*   Extracted attributes include:
    
    *   Assessment name
        
    *   Assessment URL
        
    *   Description
        
    *   Duration
        
    *   Test type
        
*   Some attributes such as _adaptive support_ and _remote support_ were unavailable for many assessments directly from the SHL catalog and are therefore left empty. This limitation is documented and handled gracefully.
    

### 2.2 Training & Test Data

The provided **training and test datasets (Excel format)** were:

*   Loaded and converted into structured CSV format
    
*   Used to validate retrieval quality and compute Recall@10
    
*   Merged with crawled catalog data to increase coverage and robustness
    

All cleaned and processed data is stored under data/processed/.

3\. System Architecture
-----------------------

The solution follows a **Retrieval-Augmented Generation (RAG)** architecture:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User Query (JD)        ↓  Query Preprocessing & Enrichment        ↓  Vector Retrieval (FAISS)        ↓  Rule-based Re-ranking        ↓  Final Recommendations (5–10)        ↓  GenAI Explanation Layer   `

This modular design ensures scalability, interpretability, and robustness.

4\. Embeddings & Retrieval
--------------------------

*   **Sentence Transformers** were used to generate dense vector embeddings for all assessment descriptions.
    
*   A **FAISS index** was built for fast similarity search.
    
*   Given a query, the system retrieves top-N candidate assessments based on cosine similarity.
    

This semantic retrieval allows the system to handle diverse and unstructured job descriptions effectively.

5\. Re-ranking & Business Logic
-------------------------------

To improve relevance beyond pure semantic similarity, a **rule-based re-ranking layer** was applied:

*   Keyword boosting (e.g., Java, Python, Sales, English)
    
*   Duration matching (e.g., preference for ~60-minute assessments)
    
*   Penalization of loosely related results
    

This hybrid approach significantly improved Recall@10 and aligns recommendations more closely with hiring constraints.

6\. GenAI Explanation Layer
---------------------------

A GenAI-based explanation module generates a **natural language justification** answering:

> “Why these assessments?”

### Key Design Principles:

*   Explanations are **strictly positive** (no missing-skill assumptions)
    
*   Justifications are grounded only in:
    
    *   Job description requirements
        
    *   Assessment descriptions
        
*   No hallucinated or unavailable assessments are mentioned
    

### LLM Constraints & Mitigation:

During development, multiple free LLM providers were evaluated (HuggingFace Inference API, Gemini, Groq). Several models were deprecated or rate-limited during implementation. To ensure robustness:

*   Errors are caught and handled gracefully
    
*   Fallback explanations are returned if the LLM is unavailable
    
*   The system architecture remains provider-agnostic
    

This reflects real-world GenAI deployment challenges and resilience strategies.

7\. Evaluation Methodology
--------------------------

The system is evaluated using **Mean Recall@10**, as required.

*   For each query in the training set:
    
    *   Top-10 recommendations are generated
        
    *   Ground-truth URLs are compared against retrieved results
        
*   Mean Recall@10 achieved: **~0.50**, with iterative improvements through re-ranking and query enrichment
    

Evaluation logic is implemented in evaluation/recall\_at\_k.py.

8\. Output Format (Critical Compliance)
---------------------------------------

To comply with SHL’s automated evaluation pipeline, predictions are saved in the **exact required CSV format**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Query,Assessment_url  Query 1,URL 1  Query 1,URL 2  Query 1,URL 3  Query 2,URL 1  ...   `

A dedicated utility ensures strict adherence to this format. Any deviation could result in automatic rejection, so this step is handled explicitly outside the UI.

9\. Deployment
--------------

*   **API Layer**: Built using FastAPI with /health and /recommend endpoints
    
*   **Frontend**: Streamlit-based UI for interactive testing
    
*   **Cloud Deployment**:
    
    *   Streamlit Cloud chosen due to free-tier compatibility and memory constraints
        
    *   Environment variables managed securely (no secrets committed)
        

This setup balances accessibility, cost, and reliability.

10\. Key Strengths of the Solution
----------------------------------

*   End-to-end RAG pipeline with real SHL data
    
*   Hybrid retrieval + re-ranking for higher accuracy
    
*   Explicit Recall@10 evaluation
    
*   Robust handling of GenAI service limitations
    
*   Strict compliance with submission format and API requirements
    
*   Clean, modular, and extensible codebase
    

11\. Conclusion
---------------

This solution demonstrates a **practical, production-oriented GenAI system** that combines information retrieval, machine learning, and LLM-based reasoning. It is designed to be robust against real-world constraints such as incomplete data and evolving LLM APIs, while strictly adhering to SHL’s technical and evaluation requirements.