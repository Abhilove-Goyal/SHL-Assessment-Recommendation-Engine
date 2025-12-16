import pandas as pd

train = pd.read_excel("data/raw/train.xlsx")
test = pd.read_excel("data/raw/test.xlsx")

train.columns = train.columns.str.strip()
test.columns = test.columns.str.strip()

train["Query"] = train["Query"].str.strip()
test["Query"] = test["Query"].str.strip()

train.to_csv("data/processed/train.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)

print("Saved processed CSV files")
