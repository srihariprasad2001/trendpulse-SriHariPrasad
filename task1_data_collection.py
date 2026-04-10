import requests
import json
import os
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# TrendPulse — Task 1: Fetch Data from HackerNews API
# Fetches top trending stories and groups them into 5 categories
# No API key needed — HackerNews is fully open
# ─────────────────────────────────────────────────────────────

# ── Category keywords (case-insensitive matching) ─────────────
CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}

MAX_STORIES_PER_CATEGORY = 25  # collect up to 25 per category = 125 total
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# ── Helper: assign category based on title keywords ──────────
def assign_category(title):
    """Check the story title against each category's keywords.
    Returns the first matching category, or None if no match found."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None  # title doesn't match any category

# ── Step 1: Fetch top story IDs ───────────────────────────────
print("Step 1: Fetching top story IDs from HackerNews...")

try:
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        headers=HEADERS
    )
    response.raise_for_status()
    all_ids = response.json()[:500]  # fetch first 500 story IDs
    print(f"   Got {len(all_ids)} story IDs")
except Exception as e:
    print(f"   Failed to fetch story IDs: {e}")
    exit()

# ── Step 2: Fetch story details and group by category ─────────
print("\nStep 2: Fetching story details and categorising...")

# Dictionary to hold collected stories per category
categorized = {cat: [] for cat in CATEGORIES}

for story_id in all_ids:
    # Stop early if all categories already have enough stories
    if all(len(stories) >= MAX_STORIES_PER_CATEGORY for stories in categorized.values()):
        break

    try:
        # Fetch details of a single story using its ID
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        res = requests.get(story_url, headers=HEADERS)
        res.raise_for_status()
        story = res.json()

        # Skip if story is empty or has no title (could be a comment/poll)
        if not story or "title" not in story:
            continue

        title = story.get("title", "")
        category = assign_category(title)

        # Save only if category matched and that bucket still needs stories
        if category and len(categorized[category]) < MAX_STORIES_PER_CATEGORY:

            # Check if this category just got filled — sleep once per category
            was_incomplete = len(categorized[category]) < MAX_STORIES_PER_CATEGORY

            categorized[category].append({
                "post_id":      story.get("id"),
                "title":        title,
                "category":     category,
                "score":        story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author":       story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # If the category just became full, wait 2 seconds before continuing
            if was_incomplete and len(categorized[category]) == MAX_STORIES_PER_CATEGORY:
                print(f"   '{category}' complete ({MAX_STORIES_PER_CATEGORY} stories). Waiting 2s...")
                time.sleep(2)

    except Exception as e:
        # If one story fails, print a message and skip — don't crash the whole script
        print(f"   Skipping story {story_id}: {e}")
        continue

# ── Step 3: Flatten all categories into one list ─────────────
all_stories = []
for cat, stories in categorized.items():
    all_stories.extend(stories)
    print(f"   {cat:15s} → {len(stories)} stories")

# ── Step 4: Save to JSON file inside data/ folder ─────────────
print("\nStep 3: Saving results to JSON file...")

# Create the data/ directory if it doesn't already exist
os.makedirs("data", exist_ok=True)

# File is named with today's date: e.g. data/trends_20240115.json
today = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today}.json"

with open(filename, "w") as f:
    json.dump(all_stories, f, indent=2)

# Final summary message
print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")
