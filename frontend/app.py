import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
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

# Initialize session state
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

            # Generate CSV (string)
            csv_text = save_submission(query, results)

            # Convert to bytes (IMPORTANT)
            st.session_state.csv_data = csv_text.encode("utf-8")

        st.success("Recommendations generated!")

        st.subheader("Recommended Assessments")
        for i, r in enumerate(results, 1):
            st.markdown(f"**{i}. {r.get('name', 'Assessment')}**")
            st.write(r.get("assessment_url", ""))

        st.subheader("Why these assessments?")
        st.write(explanation)

# ✅ Download button only appears when CSV exists
st.session_state.csv_data = csv_text.encode("utf-8") if csv_text else None

if st.session_state.csv_data:
    st.download_button(
        "Download Submission CSV",
        st.session_state.csv_data,
        file_name="shl_submission.csv",
        mime="text/csv"
    )

