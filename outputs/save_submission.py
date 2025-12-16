import csv
import os
import io
import io
SUBMISSION_FILE = "outputs/submission.csv"
# csv_data = save_submission(query, results)
def save_submission(query, results):
    """
    Returns CSV content as string in SHL-required format
    """
    output = io.StringIO()
    writer = csv.writer(output)

    for r in results:
        writer.writerow([query, r["assessment_url"]])

    return output.getvalue()

