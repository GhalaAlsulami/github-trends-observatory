import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="GitHub Trends Observatory",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# CUSTOM CSS — magazine feel
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* Page background */
    .stApp { background-color: #f8f9fa; }

    /* Hide streamlit default header */
    header[data-testid="stHeader"] { background: transparent; }

    /* Main container */
    .block-container { padding-top: 2rem; max-width: 1100px; }

    /* Hero headline */
    .hero-headline {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1a1a2e;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }

    /* Hero subheadline */
    .hero-sub {
        font-size: 1.1rem;
        color: #4a4a6a;
        margin-bottom: 0.3rem;
        line-height: 1.6;
    }

    /* Edition label */
    .edition-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 1rem;
    }

    /* Section title */
    .section-title {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.8rem;
        margin-top: 0.5rem;
    }

    /* Divider */
    .mag-divider {
        border: none;
        border-top: 2px solid #1a1a2e;
        margin: 0.5rem 0 1.5rem 0;
    }

    /* Thin divider */
    .thin-divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }

    /* Power ranking row */
    .rank-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    .rank-card:hover { transform: translateX(4px); }

    .rank-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #e0e0e0;
        min-width: 48px;
    }
    .rank-number.top { color: #1a1a2e; }

    .rank-lang {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a2e;
        flex: 1;
    }

    .rank-count {
        font-size: 0.95rem;
        color: #666;
        min-width: 100px;
        text-align: right;
    }

    .trend-up { color: #2ecc71; font-size: 1.1rem; font-weight: 700; }
    .trend-down { color: #e74c3c; font-size: 1.1rem; font-weight: 700; }
    .trend-neu { color: #bbb; font-size: 1.1rem; }

    /* Featured repo card */
    .repo-card {
        background: #1a1a2e;
        color: white;
        border-radius: 16px;
        padding: 28px 32px;
        box-shadow: 0 4px 20px rgba(26,26,46,0.15);
    }
    .repo-card-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 12px;
    }
    .repo-card-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    .repo-card-stars {
        font-size: 1rem;
        color: #f39c12;
        margin-bottom: 12px;
    }
    .repo-card-lang {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        color: #ddd;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-bottom: 16px;
    }
    .repo-card-insight {
        font-size: 0.95rem;
        color: #aaa;
        line-height: 1.6;
    }

    /* Stat pill */
    .stat-pill {
        background: white;
        border-radius: 50px;
        padding: 10px 20px;
        display: inline-block;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin: 4px;
        font-size: 0.9rem;
        color: #333;
    }
    .stat-pill strong { color: #1a1a2e; }

    /* Surge card */
    .surge-card {
        background: linear-gradient(135deg, #fff8e1, #fff3cd);
        border: 2px solid #f39c12;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .surge-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #f39c12;
        margin-bottom: 6px;
    }
    .surge-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a2e;
    }

    /* Insight box */
    .insight-box {
        background: #eef2ff;
        border-left: 4px solid #4361ee;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 12px 0;
        font-size: 0.92rem;
        color: #2d3561;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
ANALYSIS_FILE = os.path.join(os.path.dirname(__file__), "data", "analysis.csv")
SNAPSHOTS_FILE = os.path.join(os.path.dirname(__file__), "data", "snapshots.csv")

@st.cache_data
def load_data():
    analysis = pd.read_csv(ANALYSIS_FILE)
    snapshots = pd.read_csv(SNAPSHOTS_FILE)
    snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])
    return analysis, snapshots

if not os.path.exists(ANALYSIS_FILE):
    st.error("No data found. Please run fetch.py and analyze.py first.")
    st.stop()

df, df_snapshots = load_data()
df = df.drop_duplicates(subset="language", keep="last").reset_index(drop=True)
# ─────────────────────────────────────────
# COMPUTED INSIGHTS
# ─────────────────────────────────────────
df_sorted = df.sort_values("total_repos", ascending=False).drop_duplicates(subset="language").reset_index(drop=True)
top_lang = df_sorted.iloc[0]
second_lang = df_sorted.iloc[1]
top_repo = df.sort_values("top_repo_stars", ascending=False).iloc[0]
total_repos = df["total_repos"].sum()
top_two_share = round(
    (df_sorted.iloc[0]["total_repos"] + df_sorted.iloc[1]["total_repos"])
    / total_repos * 100, 1
)
days_of_data = df_snapshots["snapshot_date"].nunique()

# Dynamic headline based on real data
def generate_headline(df_sorted, top_repo):
    top = df_sorted.iloc[0]
    second = df_sorted.iloc[1]
    ratio = round(top["total_repos"] / second["total_repos"], 1)
    return (
        f"{top['language']} leads GitHub with "
        f"{top['total_repos']:,} repos — "
        f"{ratio}x ahead of {second['language']}."
    )

def generate_subheadline(top_repo, df_sorted):
    return (
        f"The most starred project right now is "
        f"{top_repo['top_repo_name']} "
        f"({int(top_repo['top_repo_stars']):,} ⭐) — "
        f"a {top_repo['language']} repo that's pulling ahead of the pack."
    )

# ─────────────────────────────────────────
# HERO — NEWSPAPER FRONT PAGE
# ─────────────────────────────────────────
today_str = datetime.today().strftime("%A, %B %d %Y").upper()

st.markdown(f'<div class="edition-label">🔭 GitHub Trends Observatory &nbsp;·&nbsp; {today_str} &nbsp;·&nbsp; Daily Edition</div>', unsafe_allow_html=True)
st.markdown('<hr class="mag-divider">', unsafe_allow_html=True)

col_hero, col_pills = st.columns([3, 1])

with col_hero:
    st.markdown(f'<div class="hero-headline">{generate_headline(df_sorted, top_repo)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{generate_subheadline(top_repo, df_sorted)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="edition-label">Based on {days_of_data} day(s) of data · {total_repos:,} repositories tracked · 10 languages</div>', unsafe_allow_html=True)

with col_pills:
    st.markdown('<div class="section-title">Tracking</div>', unsafe_allow_html=True)
    langs_html = "".join([
        f'<span style="display:inline-block;background:#1a1a2e;color:white;'
        f'padding:4px 10px;border-radius:20px;font-size:11px;'
        f'margin:2px;font-weight:500">{row["language"]}</span>'
        for _, row in df_sorted.iterrows()
    ])
    st.markdown(langs_html, unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 1 — POWER RANKINGS + REPO OF THE DAY
# ─────────────────────────────────────────
col_rank, col_repo = st.columns([1.2, 1])

with col_rank:
    st.markdown('<div class="section-title">The Power Rankings</div>', unsafe_allow_html=True)
    st.markdown("**Which languages own GitHub right now?**")
    st.caption("Ranked by total number of repositories with 10+ stars")

    for i, row in df_sorted.iterrows():
        rank = i + 1
        bar_pct = int((row["total_repos"] / df_sorted.iloc[0]["total_repos"]) * 100)
        trend_html = '<span class="trend-neu">—</span>'
        if "trend" in df.columns:
            if row.get("trend") == "rising":
                trend_html = '<span class="trend-up">↑</span>'
            elif row.get("trend") == "declining":
                trend_html = '<span class="trend-down">↓</span>'

        rank_class = "top" if rank <= 3 else ""
        st.markdown(f"""
        <div class="rank-card">
            <div class="rank-number {rank_class}">#{rank}</div>
            <div style="flex:1">
                <div class="rank-lang">{row['language']}</div>
                <div style="background:#f0f0f0;border-radius:4px;height:4px;margin-top:6px;width:100%">
                    <div style="background:#1a1a2e;height:4px;border-radius:4px;width:{bar_pct}%"></div>
                </div>
            </div>
            <div class="rank-count">{int(row['total_repos']):,} repos</div>
            <div style="margin-left:12px">{trend_html}</div>
        </div>
        """, unsafe_allow_html=True)

with col_repo:
    st.markdown('<div class="section-title">Repo of the Day</div>', unsafe_allow_html=True)
    st.markdown("**The project developers are obsessing over**")
    st.caption("Most starred repository across all tracked languages today")

    repo_insight = (
        f"With {int(top_repo['top_repo_stars']):,} stars, this {top_repo['language']} "
        f"project is the most watched repo across all 10 tracked languages today. "
        f"Star counts like this don't happen by accident — this is where developer "
        f"attention is concentrated right now."
    )

    st.markdown(f"""
    <div class="repo-card">
        <div class="repo-card-label">Featured Repository</div>
        <div class="repo-card-name">{top_repo['top_repo_name'].split('/')[1]}</div>
        <div class="repo-card-stars">⭐ {int(top_repo['top_repo_stars']):,} stars</div>
        <div class="repo-card-lang">{top_repo['language']}</div>
        <div class="repo-card-insight">{repo_insight}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"[View on GitHub →]({top_repo['top_repo_url']})")

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 2 — ECOSYSTEM MAP
# ─────────────────────────────────────────
st.markdown('<div class="section-title">The Ecosystem Map</div>', unsafe_allow_html=True)
st.markdown("**How is GitHub split between languages?**")
st.caption("Each language's share of total repositories tracked")

col_chart, col_insight = st.columns([1.5, 1])

with col_chart:
    fig_eco = px.pie(
        df_sorted,
        names="language",
        values="total_repos",
        hole=0.55,
        color_discrete_sequence=[
            "#1a1a2e", "#16213e", "#0f3460", "#533483",
            "#2ecc71", "#3498db", "#e74c3c", "#f39c12",
            "#9b59b6", "#1abc9c"
        ]
    )
    fig_eco.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont_size=10,
        insidetextorientation="radial",
        pull=[0.03] * len(df_sorted)
    )
    fig_eco.add_annotation(
        text=f"<b>{total_repos:,}</b><br>repos",
        x=0.5, y=0.5,
        font_size=14,
        showarrow=False
    )
    fig_eco.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.0,
            y=0.5,
            font=dict(size=11)
        ),
        height=400,
        margin=dict(l=20, r=140, t=40, b=40)
    )
    st.plotly_chart(fig_eco, use_container_width=True)

with col_insight:
    st.markdown("<br><br>", unsafe_allow_html=True)

    top3 = df_sorted.head(3)
    top3_share = round(top3["total_repos"].sum() / total_repos * 100, 1)
    bottom3 = df_sorted.tail(3)

    st.markdown(f"""
    <div class="insight-box">
        <strong>{top_lang['language']} + {second_lang['language']}</strong> account for 
        <strong>{top_two_share}%</strong> of all tracked repositories — 
        the rest of the 10 languages share the remaining {100 - top_two_share}%.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
        The top 3 languages (<strong>{', '.join(top3['language'].tolist())}</strong>) 
        dominate with <strong>{top3_share}%</strong> of total repos, 
        leaving the remaining 7 languages to compete for just {100 - top3_share}%.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
        <strong>{bottom3.iloc[0]['language']}, {bottom3.iloc[1]['language']}, 
        and {bottom3.iloc[2]['language']}</strong> are the smallest players — 
        but smaller communities often mean higher repo quality and more focused builders.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 3 — STAR LEADERBOARD
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Star Leaderboard</div>', unsafe_allow_html=True)
st.markdown("**The projects developers love most right now**")
st.caption("Top starred repository per language — these are the projects commanding the most attention")

df_stars = df.sort_values("top_repo_stars", ascending=False)[
    ["language", "top_repo_name", "top_repo_stars", "top_repo_url"]
].reset_index(drop=True)
df_stars.index += 1
df_stars.columns = ["Language", "Repo", "Stars", "URL"]

st.dataframe(
    df_stars,
    column_config={
        "URL": st.column_config.LinkColumn(
            "Open on GitHub",
            display_text="View repo"
        ),
        "Stars": st.column_config.NumberColumn(
            "Stars",
            format="%d ⭐"
        ),
    },
    use_container_width=True,
    height=420
)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 4 — TREND LINES
# ─────────────────────────────────────────
st.markdown('<div class="section-title">The Long Game</div>', unsafe_allow_html=True)
st.markdown("**Who's rising and who's falling over time?**")

if days_of_data > 1:
    st.caption(f"Tracking {days_of_data} days of data — lines will get clearer every day")

    fig_trend = go.Figure()
    for lang in df_snapshots["language"].unique():
        lang_df = df_snapshots[df_snapshots["language"] == lang].sort_values("snapshot_date")
        first = lang_df.iloc[0]["total_repos"]
        last = lang_df.iloc[-1]["total_repos"]
        color = "#2ecc71" if last > first else "#e74c3c" if last < first else "#aaa"

        fig_trend.add_trace(go.Scatter(
            x=lang_df["snapshot_date"],
            y=lang_df["total_repos"],
            name=lang,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=6)
        ))

    fig_trend.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig_trend, use_container_width=True)

else:
    col_msg, col_prev = st.columns([1, 1.5])
    with col_msg:
        st.markdown("""
        <div class="insight-box">
            <strong>This chart is building itself.</strong><br><br>
            Every day GitHub Actions runs automatically and adds a new data point. 
            After 7 days you'll see clear trend lines. After 30 days you'll be able 
            to confidently say which languages are winning and which are losing ground.<br><br>
            <strong>Come back tomorrow — it'll already look different.</strong>
        </div>
        """, unsafe_allow_html=True)
    with col_prev:
        st.caption("Today's baseline — this becomes your first trend line")
        fig_prev = px.bar(
            df_snapshots.sort_values("total_repos", ascending=False),
            x="language", y="total_repos",
            color="language",
            color_discrete_sequence=[
                "#1a1a2e", "#16213e", "#0f3460", "#533483",
                "#2ecc71", "#3498db", "#e74c3c", "#f39c12",
                "#9b59b6", "#1abc9c"
            ],
            labels={"total_repos": "Repos", "language": ""}
        )
        fig_prev.update_layout(
            showlegend=False, height=280,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_prev, use_container_width=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 5 — SURGE ALERTS
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Today\'s Anomaly</div>', unsafe_allow_html=True)
st.markdown("**Anything unusual happening in the ecosystem today?**")

if "is_surge" in df.columns and df["is_surge"].eq("YES").any():
    surge_langs = df[df["is_surge"] == "YES"]
    for _, row in surge_langs.iterrows():
        st.markdown(f"""
        <div class="surge-card">
            <div class="surge-label">⚡ Surge Detected</div>
            <div class="surge-title">{row['language']} is spiking above its normal activity level</div>
            <div style="margin-top:8px;color:#666;font-size:0.9rem">
                {int(row['total_repos']):,} repos today — unusually high compared to recent averages.
                Something is driving developers toward {row['language']} right now.
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:20px 24px;
    box-shadow:0 1px 3px rgba(0,0,0,0.06);color:#999;font-size:0.95rem">
        ✅ &nbsp; No anomalies detected today. All languages are within their normal activity ranges.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;color:#aaa;font-size:0.8rem;padding-bottom:2rem">
    GitHub Developer Trends Observatory &nbsp;·&nbsp; 
    Data from GitHub Search API &nbsp;·&nbsp; 
    Updated daily via GitHub Actions &nbsp;·&nbsp;
    Built with Python, Streamlit & Plotly &nbsp;·&nbsp;
    {today_str}
</div>
""", unsafe_allow_html=True)
