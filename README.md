# 🔭 GitHub Developer Trends Observatory

> Every developer asks the same question: *what should I learn next?*  
> Nobody had a real-time answer. So I built one.

**[→ See it live](https://app-trends-observatory-hvg3igdqjvxr6qgwx5yptq.streamlit.app/)**

---

## The Problem

The tech world moves fast — but most trend data is either outdated, paywalled, or just someone's opinion on Twitter.

There's no simple, visual, daily answer to questions like:
- Is Rust actually growing or just hyped?
- Which languages are developers actually building with *right now*?
- What project has the entire GitHub community obsessing over today?

I wanted data. Real data. Updated every single day. So I built a system that collects it automatically.

---

## The Idea

What if you could open a dashboard every morning and get a clear, honest picture of where the developer ecosystem is moving — no opinions, just numbers?

That's the GitHub Developer Trends Observatory. It tracks 10 programming languages across GitHub daily, measures which are rising and which are slowing down, and surfaces the projects commanding the most attention right now.

It doesn't just show you a snapshot — it builds a living dataset that gets more valuable every day it runs.

---

## The Solution

Every morning at 9am, an automated pipeline wakes up and:

1. Queries the GitHub API for each of the 10 tracked languages
2. Records repo counts, star counts, and top projects
3. Runs an analysis to detect trends, rankings, and unusual activity spikes
4. Commits the updated data back to this repository automatically
5. The dashboard reads the latest data — no manual work, ever

The result is a dataset that grows by itself. The longer it runs, the richer the story it tells.

---

## What It Reveals

Even with just a few days of data, the findings are already interesting:

- **Python dominates** with 43% of all tracked repositories — more than TypeScript and JavaScript combined
- **TypeScript is the real challenger** — it's closing the gap on Python faster than any other language
- **The most starred repo right now** isn't from the language you'd expect — a TypeScript project called openclaw is pulling ahead of everything with 367k stars
- **Rust is punching above its weight** — small repo count, but unusually high star velocity

These aren't opinions. They're measurements.

---

## Why It Matters

This project exists because I believe data literacy means more than cleaning datasets — it means building systems that *generate* insight continuously, not just once.

A one-time analysis is a photograph. This is a time-lapse.

---

## Built With

Python · GitHub API · pandas · Streamlit · Plotly · GitHub Actions

---

## How to Run It

```bash
git clone https://github.com/GhalaAlsulami/github-trends-observatory.git
cd github-trends-observatory
pip install -r requirements.txt
python fetch.py && python analyze.py
streamlit run dashboard.py
```

---

*Data refreshes daily · Automated with GitHub Actions · Dashboard hosted on Streamlit Cloud*

**Built by [Ghala Alsulami](https://github.com/GhalaAlsulami)**
