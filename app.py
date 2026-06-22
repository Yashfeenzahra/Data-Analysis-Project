import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Netflix Titles Dashboard",
    page_icon="🎬",
    layout="wide",
)

sns.set_style("whitegrid")
NETFLIX_RED = "#E50914"
NETFLIX_BLACK = "#221F1F"

# ---------------------------------------------------------------
# DATA LOADING + CLEANING (cached so it only runs once)
# ---------------------------------------------------------------
@st.cache_data
def load_raw_data():
    df = pd.read_csv("netflix_titles.csv")
    return df


@st.cache_data
def clean_data(df_raw: pd.DataFrame):
    df = df_raw.copy()

    before_dupes = df.shape[0]
    df = df.drop_duplicates()
    after_dupes = df.shape[0]

    missing_before = df.isnull().sum()

    for col in ["director", "cast", "country"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    df = df.dropna(subset=["date_added", "rating"])

    missing_after = df.isnull().sum()

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df = df.rename(columns={"show_id": "id", "listed_in": "genre"})
    df = df.drop(columns=[c for c in ["description"] if c in df.columns])

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)
    df["year_added"] = df["date_added"].dt.year

    info = {
        "before_dupes": before_dupes,
        "after_dupes": after_dupes,
        "missing_before": missing_before,
        "missing_after": missing_after,
    }
    return df, info


raw_df = load_raw_data()
df, clean_info = clean_data(raw_df)
movies = df[df["type"] == "Movie"]
tv = df[df["type"] == "TV Show"]

# ---------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------
st.sidebar.title("🎬 Netflix Titles")
st.sidebar.markdown(
    "A dashboard covering **data cleaning**, **data analysis**, "
    "and **data visualization** for the Netflix titles dataset."
)
st.sidebar.metric("Rows (cleaned)", df.shape[0])
st.sidebar.metric("Columns (cleaned)", df.shape[1])
st.sidebar.download_button(
    "⬇️ Download cleaned CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="netflix_titles_cleaned.csv",
    mime="text/csv",
)

# ---------------------------------------------------------------
# TABS
# ---------------------------------------------------------------
tab_overview, tab_clean, tab_analysis, tab_viz = st.tabs(
    ["🏠 Overview", "🧹 Data Cleaning", "📊 Data Analysis", "📈 Data Visualization"]
)

# =================================================================
# TAB 1 — OVERVIEW
# =================================================================
with tab_overview:
    st.title("Netflix Titles — End-to-End Dashboard")
    st.markdown(
        """
        This app walks through the full pipeline used on the **Netflix Titles** dataset:

        1. **Data Cleaning** — duplicates removed, missing values handled, columns renamed.
        2. **Data Analysis** — summary stats, category breakdowns, trends, correlations.
        3. **Data Visualization** — charts exploring the cleaned data.

        Use the tabs above to explore each stage.
        """
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Total titles (raw)", raw_df.shape[0])
    col2.metric("Total titles (cleaned)", df.shape[0])
    col3.metric("Unique titles", df["title"].nunique())

    st.subheader("Cleaned data preview")
    st.dataframe(df.head(20), use_container_width=True)

# =================================================================
# TAB 2 — DATA CLEANING
# =================================================================
with tab_clean:
    st.header("🧹 Data Cleaning")

    st.subheader("Raw data")
    st.write(f"Shape: **{raw_df.shape[0]} rows × {raw_df.shape[1]} columns**")
    st.dataframe(raw_df.head(10), use_container_width=True)

    st.subheader("1. Remove duplicate rows")
    c1, c2 = st.columns(2)
    c1.metric("Rows before", clean_info["before_dupes"])
    c2.metric("Rows after", clean_info["after_dupes"])

    st.subheader("2. Handle missing values")
    st.markdown(
        "- `director`, `cast`, `country` → filled with **\"Unknown\"**\n"
        "- Rows missing `date_added` or `rating` → dropped (small number of rows)"
    )
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("**Missing values — before**")
        st.dataframe(clean_info["missing_before"].rename("missing"))
    with mc2:
        st.markdown("**Missing values — after**")
        st.dataframe(clean_info["missing_after"].rename("missing"))

    st.subheader("3. Standardize column names")
    st.markdown(
        "Columns lowercased, stripped, spaces → underscores, and renamed:\n"
        "- `show_id` → `id`\n"
        "- `listed_in` → `genre`"
    )
    st.code(", ".join(df.columns.tolist()))

    st.subheader("4. Drop unneeded columns")
    st.markdown("Dropped: `description`")

    st.subheader("✅ Final cleaned dataset")
    st.write(f"Shape: **{df.shape[0]} rows × {df.shape[1]} columns**")
    st.dataframe(df.head(20), use_container_width=True)

# =================================================================
# TAB 3 — DATA ANALYSIS
# =================================================================
with tab_analysis:
    st.header("📊 Data Analysis")

    # --- Total records ---
    st.subheader("Total records")
    total_records = df.shape[0]
    unique_titles = df["title"].nunique()
    a1, a2 = st.columns(2)
    a1.metric("Total records", total_records)
    a2.metric("Unique titles", unique_titles)
    if total_records != unique_titles:
        st.info("Note: some titles repeat in the dataset.")
    else:
        st.success("All titles are unique.")

    # --- Highest / lowest values ---
    st.subheader("Highest and lowest values")
    longest_movie = movies.loc[movies["duration_value"].idxmax()]
    shortest_movie = movies.loc[movies["duration_value"].idxmin()]
    most_seasons = tv.loc[tv["duration_value"].idxmax()]

    b1, b2, b3 = st.columns(3)
    b1.metric("Longest movie", longest_movie["title"], f"{longest_movie['duration_value']:.0f} min")
    b2.metric("Shortest movie", shortest_movie["title"], f"{shortest_movie['duration_value']:.0f} min")
    b3.metric("Most seasons (TV)", most_seasons["title"], f"{most_seasons['duration_value']:.0f} seasons")

    # --- Averages ---
    st.subheader("Averages")
    avg_movie_duration = movies["duration_value"].mean()
    avg_tv_seasons = tv["duration_value"].mean()
    c1, c2 = st.columns(2)
    c1.metric("Average movie duration", f"{avg_movie_duration:.1f} min")
    c2.metric("Average seasons per TV show", f"{avg_tv_seasons:.2f}")

    # --- Category-wise analysis ---
    st.subheader("Category-wise analysis")
    cat1, cat2, cat3 = st.columns(3)
    with cat1:
        st.markdown("**Titles by type**")
        st.dataframe(df["type"].value_counts())
    with cat2:
        st.markdown("**Titles by rating**")
        st.dataframe(df["rating"].value_counts())
    with cat3:
        st.markdown("**Top 10 producing countries**")
        country_series = df["country"].str.split(", ").explode()
        st.dataframe(country_series.value_counts().head(10))

    # --- Trend analysis ---
    st.subheader("Trend analysis")
    titles_per_year = df["date_added"].dt.year.value_counts().sort_index()
    st.markdown("**Titles added to Netflix, per year**")
    st.bar_chart(titles_per_year)

    recent_year = int(df["date_added"].dt.year.max())
    monthly = (
        df[df["date_added"].dt.year == recent_year]["date_added"]
        .dt.month.value_counts()
        .sort_index()
    )
    st.markdown(f"**Titles added by month in {recent_year}**")
    st.bar_chart(monthly)

    # --- Correlation analysis ---
    st.subheader("Correlation analysis")
    movie_corr = movies[["release_year", "duration_value"]].corr().iloc[0, 1]
    tv_corr = tv[["release_year", "duration_value"]].corr().iloc[0, 1]
    d1, d2 = st.columns(2)
    d1.metric("Release year vs movie duration", f"{movie_corr:.3f}")
    d2.metric("Release year vs TV seasons", f"{tv_corr:.3f}")
    st.caption("A value near 0 means little to no relationship; closer to 1 or -1 means a stronger trend.")

    # --- Most frequent values ---
    st.subheader("Most frequent values")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("**Top 10 genres**")
        genre_series = df["genre"].str.split(", ").explode()
        st.dataframe(genre_series.value_counts().head(10))
    with f2:
        st.markdown("**Top 10 directors (excluding Unknown)**")
        director_counts = df[df["director"] != "Unknown"]["director"].value_counts().head(10)
        st.dataframe(director_counts)

# =================================================================
# TAB 4 — DATA VISUALIZATION
# =================================================================
with tab_viz:
    st.header("📈 Data Visualization")

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("**Movies vs TV Shows (count)**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x="type", data=df, hue="type", legend=False,
                       palette=[NETFLIX_RED, NETFLIX_BLACK], ax=ax)
        ax.set_xlabel("Type")
        ax.set_ylabel("Count")
        fig.tight_layout()
        st.pyplot(fig)

    with row1_col2:
        st.markdown("**Share of Movies vs TV Shows**")
        fig, ax = plt.subplots(figsize=(6, 6))
        df["type"].value_counts().plot(
            kind="pie", autopct="%1.1f%%", colors=[NETFLIX_RED, NETFLIX_BLACK], ax=ax
        )
        ax.set_ylabel("")
        fig.tight_layout()
        st.pyplot(fig)

    st.markdown("**Titles added to Netflix per year**")
    yearly = df["year_added"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(yearly.index, yearly.values, marker="o", color=NETFLIX_RED)
    ax.set_xlabel("Year Added")
    ax.set_ylabel("Number of Titles")
    fig.tight_layout()
    st.pyplot(fig)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("**Distribution of release years**")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(df["release_year"], bins=30, color=NETFLIX_RED, ax=ax)
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Frequency")
        fig.tight_layout()
        st.pyplot(fig)

    with row2_col2:
        st.markdown("**Correlation heatmap (numeric columns)**")
        numeric_df = df.select_dtypes(include="number")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="Reds", ax=ax)
        fig.tight_layout()
        st.pyplot(fig)
