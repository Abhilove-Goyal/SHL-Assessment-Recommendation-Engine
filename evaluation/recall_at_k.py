import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from recommender.retrieval import retrieve

TRAIN_PATH = "data/processed/train.csv"

def recall_at_k(predicted, actual, k=10):
    predicted = predicted[:k]
    return len(set(predicted) & set(actual)) / len(actual)

def main():
    train = pd.read_csv(TRAIN_PATH)

    grouped = train.groupby("Query")["Assessment_url"].apply(list)

    scores = []

    for query, true_urls in grouped.items():
        results = retrieve(query, top_k=10)
        predicted_urls = [r["assessment_url"] for r in results]

        score = recall_at_k(predicted_urls, true_urls)
        scores.append(score)

        print(f"Recall@10 for query: {score:.2f}")

    mean_recall = sum(scores) / len(scores)
    print("\n==============================")
    print(f"Mean Recall@10: {mean_recall:.4f}")
    print("==============================")

if __name__ == "__main__":
    main()
