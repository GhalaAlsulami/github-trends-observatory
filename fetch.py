#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from datetime import datetime
import os


# In[2]:


# GitHub API base URL
BASE_URL = "https://api.github.com/search/repositories"

# Languages we want to track
LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Rust", "Go",
    "Java", "C++", "Kotlin", "Swift", "Ruby"
]

# Where to save the data
OUTPUT_FILE = "data/snapshots.csv"


# In[3]:


def fetch_language_stats(language):
    """
    Fetch repo stats for a given language from GitHub API.
    Returns a dictionary with the stats we care about.
    """

    # Search for repos created in the last 7 days for this language
    query = f"language:{language} created:>2024-01-01 stars:>10"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching {language}: {response.status_code}")
        return None

    data = response.json()

    return {
        "language": language,
        "total_repos": data["total_count"],
        "top_repo_name": data["items"][0]["full_name"] if data["items"] else None,
        "top_repo_stars": data["items"][0]["stargazers_count"] if data["items"] else 0,
        "top_repo_url": data["items"][0]["html_url"] if data["items"] else None,
        "top_repo_description": data["items"][0]["description"] if data["items"] else None,
        "snapshot_date": datetime.today().strftime("%Y-%m-%d")
    }


# In[4]:


# Test with just Python first
test = fetch_language_stats("Python")
print(test)


# In[5]:


# Fetch stats for all languages
print("Fetching data from GitHub API...")

all_stats = []

for language in LANGUAGES:
    print(f"  Fetching {language}...")
    stats = fetch_language_stats(language)
    if stats:
        all_stats.append(stats)

print(f"\nDone! Got data for {len(all_stats)} languages.")


# In[6]:


# Convert to a pandas DataFrame
df_today = pd.DataFrame(all_stats)

# Preview it
df_today


# In[7]:


# Check if the CSV already exists
if os.path.exists(OUTPUT_FILE):
    # File exists — load it and append today's data
    df_existing = pd.read_csv(OUTPUT_FILE)
    df_combined = pd.concat([df_existing, df_today], ignore_index=True)
    print(f"Appended to existing file. Total rows: {len(df_combined)}")
else:
    # First time — just save today's data
    df_combined = df_today
    print(f"Created new file with {len(df_combined)} rows.")

# Save to CSV
df_combined.to_csv(OUTPUT_FILE, index=False)
print(f"Saved to {OUTPUT_FILE}")


# In[8]:


# Read it back and confirm it looks right
df_check = pd.read_csv(OUTPUT_FILE)
print(f"Rows in file: {len(df_check)}")
print(f"Columns: {list(df_check.columns)}")
df_check


# In[ ]:




