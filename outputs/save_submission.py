import csv
import os
import io
import io
SUBMISSION_FILE = "outputs/submission.csv"
# csv_data = save_submission(query, results)
def save_submission(query, results):
    output = io.StringIO()
    writer = csv.writer(output)

    for r in results:
        url = r.get("assessment_url") or r.get("url")
        if url:
            writer.writerow([query, url])

    return output.getvalue()

