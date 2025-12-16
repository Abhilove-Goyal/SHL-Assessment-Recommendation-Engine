import csv
import os

SUBMISSION_FILE = "outputs/submission.csv"

def save_submission(query, recommendations):
    file_exists = os.path.exists(SUBMISSION_FILE)

    with open(SUBMISSION_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # header only once
        if not file_exists:
            writer.writerow(["Query", "Assessment_url"])

        for rec in recommendations:
            writer.writerow([query, rec["assessment_url"]])
