import csv
import os
import io
SUBMISSION_FILE = "outputs/submission.csv"

csv_data = save_submission(query, results)

st.download_button(
    label="Download Submission CSV",
    data=csv_data,
    file_name="shl_submission.csv",
    mime="text/csv"
)

