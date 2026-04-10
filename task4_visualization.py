import pandas as pd
import matplotlib.pyplot as plt
import os

# ─────────────────────────────────────────────────────────────
# TrendPulse — Task 4: Visualizations
# Creates 3 charts + bonus dashboard from trends_analysed.csv
# ─────────────────────────────────────────────────────────────

# ── Step 1: Setup ─────────────────────────────────────────────

# Load the analysed CSV produced by Task 3
df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} stories for visualization")

# Create the outputs/ folder if it doesn't already exist
os.makedirs("outputs", exist_ok=True)

# ── Chart 1: Top 10 Stories by Score (Horizontal Bar Chart) ──

# Sort by score and take the top 10 stories
top10 = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters to keep chart readable
top10["short_title"] = top10["title"].apply(
    lambda t: t[:47] + "..." if len(t) > 50 else t
)

fig1, ax1 = plt.subplots(figsize=(12, 6))

# Plot horizontal bars — highest score at the top
bars = ax1.barh(top10["short_title"], top10["score"], color="steelblue", edgecolor="white")

# Add score values at the end of each bar for easy reading
for bar in bars:
    width = bar.get_width()
    ax1.text(width + 100, bar.get_y() + bar.get_height() / 2,
             f"{width:,}", va="center", fontsize=9)

ax1.set_xlabel("Score (Upvotes)", fontsize=12)
ax1.set_ylabel("Story Title", fontsize=12)
ax1.set_title("Top 10 HackerNews Stories by Score", fontsize=14, fontweight="bold")
ax1.invert_yaxis()  # highest score appears at the top
plt.tight_layout()

# Save before show — required by assignment
plt.savefig("outputs/chart1_top_stories.png", dpi=150)
plt.show()
print("Saved: outputs/chart1_top_stories.png")


# ── Chart 2: Stories per Category (Bar Chart) ─────────────────

# Count how many stories belong to each category
category_counts = df["category"].value_counts()

# Use a different colour for each category bar
colours = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]

fig2, ax2 = plt.subplots(figsize=(8, 5))

bars2 = ax2.bar(category_counts.index, category_counts.values,
                color=colours[:len(category_counts)], edgecolor="white")

# Add count labels on top of each bar
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.3,
             str(int(height)), ha="center", va="bottom", fontsize=11)

ax2.set_xlabel("Category", fontsize=12)
ax2.set_ylabel("Number of Stories", fontsize=12)
ax2.set_title("Number of Stories per Category", fontsize=14, fontweight="bold")
plt.tight_layout()

# Save before show
plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.show()
print("Saved: outputs/chart2_categories.png")


# ── Chart 3: Score vs Comments (Scatter Plot) ─────────────────

# Split data into popular and non-popular stories using is_popular column
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(10, 6))

# Plot non-popular stories in grey
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="grey", alpha=0.6, label="Not Popular", s=60)

# Plot popular stories in orange to stand out
ax3.scatter(popular["score"], popular["num_comments"],
            color="darkorange", alpha=0.8, label="Popular", s=80)

ax3.set_xlabel("Score (Upvotes)", fontsize=12)
ax3.set_ylabel("Number of Comments", fontsize=12)
ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold")
ax3.legend(title="Popularity", fontsize=10)
plt.tight_layout()

# Save before show
plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.show()
print("Saved: outputs/chart3_scatter.png")


# ── Bonus: Combined Dashboard ─────────────────────────────────
# Combine all 3 charts into one single figure for a full dashboard

fig, axes = plt.subplots(1, 3, figsize=(22, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.02)

# --- Dashboard Panel 1: Top 10 Stories ---
axes[0].barh(top10["short_title"], top10["score"], color="steelblue", edgecolor="white")
axes[0].set_xlabel("Score")
axes[0].set_title("Top 10 Stories by Score", fontweight="bold")
axes[0].invert_yaxis()

# --- Dashboard Panel 2: Stories per Category ---
axes[1].bar(category_counts.index, category_counts.values,
            color=colours[:len(category_counts)], edgecolor="white")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
axes[1].set_title("Stories per Category", fontweight="bold")

# --- Dashboard Panel 3: Score vs Comments Scatter ---
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="grey", alpha=0.6, label="Not Popular", s=50)
axes[2].scatter(popular["score"], popular["num_comments"],
                color="darkorange", alpha=0.8, label="Popular", s=60)
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].set_title("Score vs Comments", fontweight="bold")
axes[2].legend(fontsize=9)

plt.tight_layout()

# Save before show
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: outputs/dashboard.png")

print("\nAll visualizations complete!")
