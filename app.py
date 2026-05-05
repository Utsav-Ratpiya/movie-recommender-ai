import streamlit as st
from recommender import hybrid_recommend, find_closest_movie, match_score
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = st.secrets("OMDB_API_KEY")

st.set_page_config(page_title="AI Movie Recommender", layout="wide")

# ==============================
# 🎨 UI
# ==============================
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h3 { color: white; }
.stTextInput input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}
.stButton button {
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender AI")
st.markdown("### 🔥 Ai Powered Movie Discovery")
st.divider()

# ==============================
# 📊 DATA
# ==============================
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
links = pd.read_csv("links.csv")

avg = ratings.groupby("movieId")["rating"].mean().reset_index()
movies = movies.merge(avg, on="movieId", how="left")
movies = movies.merge(links, on="movieId", how="left")

# ==============================
# 🎭 SIDEBAR GENRES
# ==============================
genres = set()
for g in movies["genres"]:
    for x in g.split("|"):
        genres.add(x)

st.sidebar.header("🎭 Genres")
for g in sorted(genres):
    st.sidebar.write(g)

# ==============================
# 🎥 OMDB (SAFE + CACHED)
# ==============================
@st.cache_data(show_spinner=False)
def fetch_details(imdb_id):
    try:
        url = f"http://www.omdbapi.com/?i=tt{str(int(imdb_id)).zfill(7)}&apikey={API_KEY}"
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return {}

def get_poster(data):
    poster = data.get("Poster")
    if poster and poster != "N/A":
        return poster
    return "https://via.placeholder.com/300x450?text=No+Image"

# ==============================
# 🔍 SEARCH
# ==============================
search = st.text_input("🎬 Search movie or mood:")

suggestions = []
if search:
    scored = []
    for title in movies["title"]:
        score = match_score(search, title)
        if score > 0:
            scored.append((title, score))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    suggestions = [x[0] for x in scored[:5]]

selected = None
for s in suggestions:
    if st.button(s, key=s):
        selected = s

movie_name = selected if selected else search

# ==============================
# 🚀 MAIN
# ==============================
if st.button("🚀 Search"):

    if movie_name:

        results = hybrid_recommend(movie_name)
        matched = find_closest_movie(movie_name)

        # 🎬 SELECTED MOVIE
        if matched:
            row = movies[movies["title"] == matched]

            if not row.empty:
                imdb_id = row["imdbId"].values[0]
                details = fetch_details(imdb_id)

                st.subheader("🎬 Your Movie")

                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image(get_poster(details), width=250)

                with col2:
                    st.subheader(matched)
                    st.write("⭐", details.get("imdbRating", "N/A"))
                    st.write("🎭", row["genres"].values[0])
                    st.write(details.get("Plot", "No description available"))

        st.divider()

        # ==============================
        # 🎯 RECOMMEND GRID (5 x 2)
        # ==============================
        st.subheader("🎯 Recommended Movies")

        results = results[:10]

        for row_idx in range(2):
            cols = st.columns(5)

            for col_idx in range(5):
                idx = row_idx * 5 + col_idx

                if idx >= len(results):
                    break

                movie = results[idx]
                r = movies[movies["title"] == movie]

                if r.empty:
                    continue

                imdb_id = r["imdbId"].values[0]
                d = fetch_details(imdb_id)

                with cols[col_idx]:
                    st.image(get_poster(d), width=160)

                    st.markdown(f"**{movie}**")

                    st.write("⭐", d.get("imdbRating", "N/A"))
                    st.write("🎭", r["genres"].values[0])

    else:
        st.warning("⚠️ Enter a movie or mood.")
