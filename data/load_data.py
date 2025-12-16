import pandas as pd

TRAIN_PATH = "data/raw/train.xlsx"
TEST_PATH = "data/raw/test.xlsx"

train_df = pd.read_excel(TRAIN_PATH)
test_df = pd.read_excel(TEST_PATH)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

print(train_df.head())
print(test_df.head())
