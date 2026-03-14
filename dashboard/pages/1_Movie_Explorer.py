import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import os

st.set_page_config(
    page_title = "Movie Explorer",
    page_icon = "🎬",
    layout = "wide"
)

emotion_colors = {
    "nostalgia"      : "#FF9B9B",
    "love"           : "#FF4B6E",
    "admiration"     : "#FFB347",
    "joy"            : "#FFD700",
    "sadness"        : "#6B9FD4",
    "grief"          : "#4A7AB5",
    "heartbreak"     : "#C154C1",
    "disappointment" : "#A0A0A0",
    "criticism"      : "#708090",
    "fascination"    : "#50C878",
    "excitement"     : "#FF7F50",
    "anger"          : "#FF4500",
    "bittersweetness": "#DDA0DD",
    "sentimentality" : "#F4A460",
    "empathy"        : "#87CEEB"
}


movie_meta = {
    "Titanic"               : {"year": 1997, "genre": "Romance / Drama"},
    "Interstellar"          : {"year": 2014, "genre": "Sci-Fi"},
    "La La Land"            : {"year": 2016, "genre": "Musical / Romance"},
    "Parasite"              : {"year": 2019, "genre": "Thriller"},
    "Schindlers List"       : {"year": 1993, "genre": "Historical Drama"},
    "Shawshank Redemption"  : {"year": 1994, "genre": "Drama"},
    "The Dark Knight"       : {"year": 2008, "genre": "Superhero"}
}


@st.cache_data
def load_emotion_data(movie_name):
    movie_slug = movie_name.lower().replace(" ", "_")
    file = f"results/emotions/{movie_slug}_emotions.csv"

    if os.path.exists(file):
        df = pd.read_csv(file, index_col = "year")
        df.index = df.index.astype(int)
        return df.sort_index()
    return None

st.sidebar.title("Movie Exploreor")
st.sidebar.markdown("Select a movie to explore its emotion evolution.")

selected_movie = st.sidebar.selectbox(
    "Choose a movie",
    list(movie_meta.keys())
)

emotions_df = load_emotion_data(selected_movie)

if emotions_df is not None:
    min_year = int(emotions_df.index.min())
    max_year = int(emotions_df.index.max())

    year_range = st.sidebar.slider(
        "Select year range",
        min_value = min_year,
        max_value = max_year,
        value = (min_year, max_year)
    )

    emotions_df = emotions_df.loc[year_range[0]:year_range[1]]

meta = movie_meta[selected_movie]
st.title(f"{selected_movie} ({meta['year']})")
st.caption(f"Genre: {meta['genre']}")
st.divider()

if emotions_df is None:
    st.error(f"No emotion data found for {selected_movie}")
    st.stop()

years = emotions_df.index.tolist()
dominant = emotions_df.idxmax(axis = 1)

col1, col2, col3 = st.columns(3)

with col1:
    most_common = dominant.value_counts().index[0]
    st.metric("Most Dominant Emotion", most_common.capitalize())

with col2:
    st.metric("Years Tracked", len(years))

with col3:
    top_year = emotions_df.max(axis =1).idxmax()
    st.metric("Most Emotional Year", str(top_year))

st.divider()

# Plot 1

st.subheader("How did people FEEL about this movie each year?")
st.caption("Each block shows the strongest emotion that year")

fig1, ax1 = plt.subplots(figsize = (16, 3))

colors = [emotion_colors.get(e, "#CCCCCC") for e in dominant]

for i, (year, emotion, color) in enumerate(zip(years, dominant, colors)):
    ax1.barh(0, 1, left = i, color = color, edgecolor = "white", linewidth = 2, height = 0.6)
    ax1.text(i + 0.5, 0.38, str(year), ha = "center", fontsize = 9, fontweight = "bold", color = "#333333")
    ax1.text(i + 0.5, 0, emotion, ha = "center", va="center", fontsize = 8, fontweight = "bold", color = "white", rotation = 90)

ax1.set_xlim(0, len(years))
ax1.set_ylim(-0.5, 0.8)
ax1.axis("off")

ax1.annotate("", xy=(len(years), -0.45), xytext = (0, -0.45), arrowprops=dict(arrowstyle = "->", color = "#333333", lw = 2))
ax1.text(len(years) / 2, -0.48, "Time ->", ha = "center", va="top", fontsize = 10, color="#333333")

unique_emotions = dominant.unique()
patches = [
    mpatches.Patch(
        color = emotion_colors.get(e, "#CCCCCC"),
        label = e.capitalize()
    )
    for e in unique_emotions
]
ax1.legend(handles=patches, loc = "lower right", fontsize = 8, ncol = 3, framealpha = 0.9, bbox_to_anchor=(1, -0.3))
st.pyplot(fig1)
plt.close()

st.divider()

# Plot 2

st.subheader("How did the dominant emotion evolve over time?")
st.caption("Highlighted line = most dominant emotion | Grey lines = all others for reference")

most_dominant = dominant.value_counts().index[0]

selected_emotion = st.selectbox(
    "HIghlight a specific emotion",
    options = emotions_df.columns.tolist(),
    index = emotions_df.columns.tolist().index(most_dominant)
)

fig2, ax2 = plt.subplots(figsize=(16, 5))

for emotion in emotions_df.columns:
    scores = emotions_df[emotion].values
    if emotion == selected_emotion:
        ax2.plot(years, scores, marker = "o", linewidth = 2.5, markersize = 6, color = emotion_colors.get("#CCCCCC"), zorder = 5)

        ax2.text(years[-1] + 0.1, scores[-1], emotion.capitalize(), va = "center", fontsize = 9, color = emotion_colors.get(emotion, "#CCCCCC"), fontweight = "bold")
    else:
        ax2.plot(years, scores, marker = "o", linewidth = 1, markersize = 3, color = "#CCCCCC", alpha = 0.5, zorder = 2)

peak_year = emotions_df[selected_emotion].idxmax()
peak_score = emotions_df[selected_emotion][peak_year]
ax2.annotate(
    f"Peak {selected_emotion} ({peak_year})",
    xy = (peak_year, peak_score),
    xytext = (peak_year - 2, peak_score + 0.05),
    arrowprops= dict(arrowstyle = "->", color = "#333333"),
    fontsize = 8, color = "#333333"
)

ax2.set_xlabel("Year", fontsize = 11)
ax2.set_ylabel("Emotion Strength", fontsize = 11)
ax2.set_xticks(years)
ax2.set_xticklabels(years, rotation = 45, fontsize = 11)
ax2.set_ylim(0, 0.5)
ax2.grid(True, alpha = 0.2, linestyle = "--")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

st.pyplot(fig2)
plt.close()

st.divider()

# Plot 3

st.subheader("Which emotion dominated the most overall?")
st.caption("% of years where this was the strongest feeling")

emotion_counts = dominant.value_counts()
emotion_pct = (emotion_counts / len(years) * 100).round(1)
bar_colors = [emotion_colors.get(e, "#CCCCCC") for e in emotion_pct.index]

fig3, ax3 = plt.subplots(figsize = (10, 4))

bars = ax3.barh(
    emotion_pct.index,
    emotion_pct.values,
    color = bar_colors,
    edgecolor = "white",
    linewidth = 1.5,
    height = 0.6
)

for bar, pct in zip(bars, emotion_pct.values):
    ax3.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{pct}% of years",
        va = "center", fontsize = 9, color = "#333333"
    )

ax3.set_xlabel("% of Years Dominant", fontsize=11)
ax3.set_xlim(0, 80)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.grid(True, alpha=0.2, axis="x", linestyle="--")

st.pyplot(fig3)
plt.close()

st.divider()
st.caption("Data sourced from Reddit and Letterboxd | Emotion analysis by facebook/bart-large-mnli")