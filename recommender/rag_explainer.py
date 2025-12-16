import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"
   # free, fast, strong

def explain_recommendations(query, results):
    context = ""
    for i, r in enumerate(results[:5], 1):
        name = (
            r.get("name")
            or r.get("assessment_name")
            or r.get("test_name")
            or "Assessment"
        )
        desc = r.get("description") or r.get("summary") or ""
        context += f"{i}. {name}: {desc}\n"

    prompt = f"""
You are an assessment recommendation assistant.

IMPORTANT RULES:
- ONLY use the assessments listed below.
- DO NOT mention any skills, tools, or assessments that are NOT listed.
- DO NOT make assumptions or suggestions.
- DO NOT say anything is missing or should be added.
- ONLY explain why the given assessments are suitable.

Job Requirement:
{query}

Recommended Assessments:
{context}

Explain clearly and concisely why these assessments are appropriate for the candidate.
"""


    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You explain assessment recommendations clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=150
    )

    return completion.choices[0].message.content
