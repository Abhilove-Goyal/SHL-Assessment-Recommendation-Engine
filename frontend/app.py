import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.title("Assessment Recommendation Engine")

query = st.text_area("Paste Job Description")

if st.button("Recommend"):
    response = requests.post(
        f"{API_BASE_URL}/recommend",
        json={"query": query},
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        st.subheader("Recommended Assessments")
        for i, r in enumerate(data["recommendations"], 1):
            st.markdown(f"**{i}. {r.get('name', 'Assessment')}**")
            st.write(r.get("assessment_url", ""))

        st.subheader("Why these assessments?")
        st.write(data["explanation"])
    else:
        st.error("API error. Please try again.")
