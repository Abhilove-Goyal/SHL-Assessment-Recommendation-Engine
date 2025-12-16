import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recommender.duration_filter import extract_duration


def rerank(results, query):
    q = query.lower()
    desired_duration = extract_duration(query)

    for r in results:
        base_score = r["score"]
        score = base_score
        url = r["assessment_url"].lower()

        heuristic_boost = 0.0

        # -------------------------
        # Light keyword boosts
        # -------------------------
        if "java" in q and "java" in url:
            heuristic_boost += 0.03
        if "sales" in q and "sales" in url:
            heuristic_boost += 0.03
        if "english" in q and "english" in url:
            heuristic_boost += 0.03
        if "personality" in q and "personality" in url:
            heuristic_boost += 0.03

        # -------------------------
        # Duration boost (light)
        # -------------------------
        if desired_duration:
            try:
                dur = int(str(r.get("duration", "")).split()[0])
                if abs(dur - desired_duration) <= 10:
                    heuristic_boost += 0.04
            except:
                pass

        # -------------------------
        # Family expansion (ONLY if semantically relevant)
        # -------------------------
        if base_score > 0.30:
            if "java" in q and any(x in url for x in ["java", "automata", "j2ee"]):
                heuristic_boost += 0.04
            if "sales" in q and any(x in url for x in ["sales", "communication", "customer"]):
                heuristic_boost += 0.04
            if "english" in q and any(x in url for x in ["english", "verbal", "comprehension"]):
                heuristic_boost += 0.04

        # -------------------------
        # Cap total boost
        # -------------------------
        heuristic_boost = min(heuristic_boost, 0.10)

        r["score"] = base_score + heuristic_boost

    return sorted(results, key=lambda x: x["score"], reverse=True)
