import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────
# TrendPulse — Task 3: Analysis with Pandas & NumPy
# Loads clean CSV, computes stats, adds new columns, saves result
# ─────────────────────────────────────────────────────────────

# ── Step 1: Load and Explore the Data ────────────────────────

# Load the cleaned CSV produced by Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print shape: how many rows and columns were loaded
print(f"Loaded data: {df.shape}")

# Print the first 5 rows to inspect the data
print("\nFirst 5 rows:")
print(df.head().to_string())

# Print average score and average num_comments across all stories
print(f"\nAverage score   : {df['score'].mean():,.0f}")
print(f"Average comments: {df['num_comments'].mean():,.0f}")

# ── Step 2: Basic Analysis with NumPy ────────────────────────
# Use NumPy functions on the score column to find patterns

scores = np.array(df["score"])  # convert score column to NumPy array

print("\n--- NumPy Stats ---")
print(f"Mean score  : {np.mean(scores):,.0f}")
print(f"Median score: {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score   : {np.max(scores):,.0f}")
print(f"Min score   : {np.min(scores):,.0f}")

# Which category has the most stories?
# value_counts() returns categories sorted by count
top_category = df["category"].value_counts()
most_common = top_category.index[0]
most_common_count = top_category.iloc[0]
print(f"\nMost stories in: {most_common} ({most_common_count} stories)")

# Which story has the most comments?
# idxmax() gives the index of the row with the highest num_comments
most_commented_idx = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]
print(f"\nMost commented story: \"{most_commented_title}\" — {most_commented_count:,} comments")

# ── Step 3: Add New Columns ───────────────────────────────────

# engagement = num_comments / (score + 1)
# Measures how much discussion a story gets per upvote
# We add 1 to score to avoid division by zero
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score, else False
# Marks stories that are above average in upvotes
average_score = df["score"].mean()
df["is_popular"] = df["score"] > average_score

# Round engagement to 4 decimal places for cleanliness
df["engagement"] = df["engagement"].round(4)

# ── Step 4: Save the Result ───────────────────────────────────

# Save updated DataFrame (with the 2 new columns) to CSV
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")
