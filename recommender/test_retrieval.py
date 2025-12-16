import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from recommender.retrieval import retrieve
query = "Hiring entry level Java developer with problem solving skills"

results = retrieve(query)

for r in results:
    print(r["name"], "|", r["assessment_url"])
