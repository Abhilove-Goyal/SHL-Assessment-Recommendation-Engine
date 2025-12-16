import re

def extract_duration(query):
    q = query.lower()

    # Match minutes
    match = re.search(r'(\d+)\s*(min|minute)', q)
    if match:
        return int(match.group(1))

    # Match hour
    if "hour" in q:
        return 60

    return None
