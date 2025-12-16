import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from recommender.retrieval import retrieve
from recommender.rerank import rerank
from recommender.rag_explainer import explain_recommendations
from outputs.save_submission import save_submission

st.set_page_config(
    page_title="SHL Assessment Recommendation Engine",
    layout="wide"
)

st.title("SHL GenAI Assessment Recommendation Engine")

query = st.text_area("Paste Job Description", height=200)
top_k = st.slider("Number of recommendations", 3, 10, 5)

# Initialize session state ONCE
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Generating recommendations..."):
            results = retrieve(query, top_k=top_k)
            results = rerank(results, query)
            explanation = explain_recommendations(query, results)

            # 🔹 Convert results to TABULAR format (CRITICAL)
            rows = []
            for r in results:
                rows.append({
                    "Query": query,
                    "Assessment_url": r["assessment_url"]
                })
            
            df = pd.DataFrame(rows)
            
            st.subheader("Recommended Assessments (Tabular Format)")
            
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Assessment_url": st.column_config.LinkColumn(
                        "Assessment URL",
                        display_text="Open assessment"
                    )
                }
            )

            # 🔹 Save CSV in memory
            st.session_state.csv_data = df.to_csv(
                index=False,
                header=False   # SHL format: no header
            ).encode("utf-8")

        st.success("Recommendations generated!")

        # 🔹 Show TABLE (SHL requirement)
        st.subheader("Recommended Assessments (Tabular Format)")
        st.dataframe(df, use_container_width=True)

        st.subheader("Why these assessments?")
        st.write(explanation)


# ✅ Render download button ONLY if CSV exists
if st.session_state.csv_data is not None:
    st.download_button(
        label="Download Submission CSV",
        data=st.session_state.csv_data,
        file_name="shl_submission.csv",
        mime="text/csv"
    )
