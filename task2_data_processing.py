import pandas as pd
import glob
import os

# ─────────────────────────────────────────────────────────────
# TrendPulse — Task 2: Clean the Data & Save as CSV
# Loads the JSON from Task 1, cleans it, saves as CSV
# ─────────────────────────────────────────────────────────────

# ── Step 1: Load the JSON file from data/ folder ─────────────
# Find the most recent trends JSON file (data/trends_YYYYMMDD.json)
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ folder. Please run task1_data_collection.py first.")
    exit()

# Pick the most recently created JSON file
latest_file = max(json_files, key=os.path.getmtime)

# Load JSON into a Pandas DataFrame
df = pd.read_json(latest_file)
print(f"Loaded {len(df)} stories from {latest_file}")

# ── Step 2: Clean the Data ────────────────────────────────────

# 2a. Remove duplicate rows based on post_id
# Same story might have been collected twice
df.drop_duplicates(subset="post_id", inplace=True)
print(f"After removing duplicates: {len(df)}")

# 2b. Drop rows where critical fields are missing
# A story without post_id, title, or score is useless
df.dropna(subset=["post_id", "title", "score"], inplace=True)
print(f"After removing nulls: {len(df)}")

# 2c. Fix data types — score and num_comments must be integers
# They may have been stored as floats after JSON loading
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# 2d. Remove low quality stories — score less than 5 is too low
# These stories have very little community engagement
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 2e. Strip extra whitespace from the title column
# Prevents issues in analysis and visualization later
df["title"] = df["title"].str.strip()

# ── Step 3: Save cleaned data as CSV ─────────────────────────
output_path = "data/trends_clean.csv"

# Save to CSV without the row index
df.to_csv(output_path, index=False)
print(f"\nSaved {len(df)} rows to {output_path}")

# Print a summary: how many stories per category
print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
