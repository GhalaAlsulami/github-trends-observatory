#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


# In[2]:


# Input and output file paths
INPUT_FILE = "data/snapshots.csv"
OUTPUT_FILE = "data/analysis.csv"

# Date ranges we'll use for analysis
TODAY = datetime.today().strftime("%Y-%m-%d")
SEVEN_DAYS_AGO = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
FOURTEEN_DAYS_AGO = (datetime.today() - timedelta(days=14)).strftime("%Y-%m-%d")

print(f"Today: {TODAY}")
print(f"7 days ago: {SEVEN_DAYS_AGO}")
print(f"14 days ago: {FOURTEEN_DAYS_AGO}")


# In[3]:


# Load snapshots
df = pd.read_csv(INPUT_FILE)

# Convert snapshot_date to proper datetime type
df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

# Quick look at what we have
print(f"Total rows: {len(df)}")
print(f"Date range: {df['snapshot_date'].min()} → {df['snapshot_date'].max()}")
print(f"Languages tracked: {df['language'].nunique()}")
df.head()


# In[4]:


# Get the most recent snapshot date
latest_date = df["snapshot_date"].max()

# Filter to only today's data
df_latest = df[df["snapshot_date"] == latest_date]

# Rank languages by total repo count
language_ranking = (
    df_latest[["language", "total_repos"]]
    .sort_values("total_repos", ascending=False)
    .reset_index(drop=True)
)

language_ranking.index += 1  # Start ranking from 1
print(f"Language ranking as of {latest_date.strftime('%Y-%m-%d')}:")
language_ranking


# In[5]:


# Sort all snapshots by stars to find the hottest repos right now
star_leaderboard = (
    df_latest[["language", "top_repo_name", "top_repo_stars", "top_repo_url", "top_repo_description"]]
    .sort_values("top_repo_stars", ascending=False)
    .reset_index(drop=True)
)

star_leaderboard.index += 1
print("Top repos by star count right now:")
star_leaderboard


# In[6]:


# Calculate the share of total repos each language represents
total_repos_all = df_latest["total_repos"].sum()

topic_pulse = df_latest[["language", "total_repos"]].copy()
topic_pulse["share_pct"] = (
    (topic_pulse["total_repos"] / total_repos_all) * 100
).round(2)
topic_pulse = topic_pulse.sort_values("share_pct", ascending=False).reset_index(drop=True)
topic_pulse.index += 1

print(f"Total repos across all tracked languages: {total_repos_all:,}")
print("\nLanguage share of ecosystem:")
topic_pulse


# In[7]:


# Group by language and sort by date to see trend direction
if df["snapshot_date"].nunique() > 1:

    trend_data = []

    for language in df["language"].unique():
        lang_df = df[df["language"] == language].sort_values("snapshot_date")

        if len(lang_df) >= 2:
            first_count = lang_df.iloc[0]["total_repos"]
            last_count = lang_df.iloc[-1]["total_repos"]
            change = last_count - first_count
            change_pct = round((change / first_count) * 100, 2)

            trend_data.append({
                "language": language,
                "repos_first_snapshot": first_count,
                "repos_latest_snapshot": last_count,
                "change": change,
                "change_pct": change_pct,
                "trend": "rising" if change > 0 else "declining" if change < 0 else "stable"
            })

    df_trends = pd.DataFrame(trend_data).sort_values("change_pct", ascending=False)
    df_trends = df_trends.reset_index(drop=True)
    df_trends.index += 1
    print("Rising vs declining languages:")
    print(df_trends)

else:
    print("Only 1 day of data so far — trend analysis needs at least 2 snapshots.")
    print("Run fetch.py again tomorrow and this will show real trends!")
    df_trends = df_latest[["language"]].copy()
    df_trends["trend"] = "pending"


# In[8]:


# Detect languages with unusually high repo counts vs their average
if df["snapshot_date"].nunique() > 1:

    surge_data = []

    for language in df["language"].unique():
        lang_df = df[df["language"] == language].sort_values("snapshot_date")

        if len(lang_df) >= 2:
            avg_repos = lang_df["total_repos"].mean()
            std_repos = lang_df["total_repos"].std()
            latest_repos = lang_df.iloc[-1]["total_repos"]

            # Z-score: how many standard deviations above average is today?
            z_score = round((latest_repos - avg_repos) / std_repos, 2) if std_repos > 0 else 0

            surge_data.append({
                "language": language,
                "average_repos": round(avg_repos),
                "latest_repos": latest_repos,
                "z_score": z_score,
                "is_surge": "YES" if z_score > 1.5 else "no"
            })

    df_surge = pd.DataFrame(surge_data).sort_values("z_score", ascending=False)
    df_surge = df_surge.reset_index(drop=True)
    print("Surge detection (z-score > 1.5 = unusual spike):")
    print(df_surge)

else:
    print("Need more than 1 snapshot for surge detection.")
    df_surge = df_latest[["language"]].copy()
    df_surge["is_surge"] = "pending"


# In[9]:


# Merge all analysis results together
df_analysis = df_latest[["language", "total_repos", "top_repo_name", 
                           "top_repo_stars", "top_repo_url", "snapshot_date"]].copy()

# Add share percentage
df_analysis = df_analysis.merge(
    topic_pulse[["language", "share_pct"]], on="language", how="left"
)

# Add trend info
df_analysis = df_analysis.merge(
    df_trends[["language", "trend"]], on="language", how="left"
)

# Add surge info
df_analysis = df_analysis.merge(
    df_surge[["language", "is_surge"]], on="language", how="left"
)

# Sort by total repos
df_analysis = df_analysis.sort_values("total_repos", ascending=False).reset_index(drop=True)

# Save
df_analysis.to_csv(OUTPUT_FILE, index=False)
print(f"Analysis saved to {OUTPUT_FILE}")
print(f"Rows: {len(df_analysis)}")
df_analysis


# In[10]:


print("=" * 50)
print("ANALYSIS COMPLETE")
print("=" * 50)
print(f"Date: {TODAY}")
print(f"Languages analyzed: {len(df_analysis)}")
print(f"\nTop language by repos: {df_analysis.iloc[0]['language']} ({df_analysis.iloc[0]['total_repos']:,} repos)")
print(f"Top repo by stars: {df_analysis.iloc[0]['top_repo_name']} ({df_analysis.iloc[0]['top_repo_stars']:,} stars)")
print(f"\nFile saved: {OUTPUT_FILE}")
print("=" * 50)


# In[ ]:




