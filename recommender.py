import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import re
import os

# ==============================
# 🔧 CLEAN TEXT
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    return clean_text(text).split()

# ==============================
# LOAD DATA
# ==============================
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# popularity
avg_ratings = ratings.groupby("movieId")["rating"].mean().reset_index()
avg_ratings.rename(columns={"rating": "avg_rating"}, inplace=True)

movies = movies.merge(avg_ratings, on="movieId", how="left")

data = pd.merge(ratings, movies, on="movieId")

movie_matrix = data.pivot_table(index='userId', columns='title', values='rating').fillna(0)
similarity = cosine_similarity(movie_matrix.T)

# ==============================
# 🔍 SEARCH SCORE
# ==============================
def match_score(query, title):
    q_tokens = tokenize(query)
    t_tokens = tokenize(title)

    score = 0
    for q in q_tokens:
        for t in t_tokens:
            if q in t:
                score += 2

    if clean_text(query) in clean_text(title):
        score += 5

    return score

def find_closest_movie(query):
    best_match = None
    best_score = 0

    for title in movie_matrix.columns:
        score = match_score(query, title)
        if score > best_score:
            best_score = score
            best_match = title

    return best_match if best_score > 0 else None

# ==============================
# 🤖 MODEL + EMBEDDINGS CACHE
# ==============================
model = SentenceTransformer('all-MiniLM-L6-v2')

movies["content"] = movies["title"] + " " + movies["genres"]

if os.path.exists("embeddings.npy"):
    embeddings = np.load("embeddings.npy")
else:
    embeddings = model.encode(movies["content"].tolist())
    np.save("embeddings.npy", embeddings)

# ==============================
# 🧠 SEMANTIC
# ==============================
def semantic_recommend(query, top_n=30):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[-top_n:][::-1]
    return movies.iloc[top_indices]["title"].tolist()

# ==============================
# 🎯 COLLABORATIVE
# ==============================
def collaborative_recommend(movie_name, top_n=30):
    idx = list(movie_matrix.columns).index(movie_name)

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return [movie_matrix.columns[i[0]] for i in scores[1:top_n+1]]

# ==============================
# 🚀 PRODUCTION RANKING
# ==============================
def hybrid_recommend(query, top_n=10):

    closest = find_closest_movie(query)

    semantic = semantic_recommend(query, 30)
    collab = collaborative_recommend(closest, 30) if closest else []

    candidates = list(dict.fromkeys(semantic + collab))

    query_tokens = tokenize(query)
    keywords = query_tokens[:2]

    movie_row = movies[movies["title"] == closest]
    input_genres = movie_row["genres"].values[0].split("|") if not movie_row.empty else []

    scored = []

    for m in candidates:
        row = movies[movies["title"] == m]
        if row.empty:
            continue

        title_tokens = tokenize(m)
        genres = row["genres"].values[0]

        score = 0

        # franchise
        if all(k in title_tokens for k in keywords):
            score += 40

        # universe
        if any(k in title_tokens for k in keywords):
            score += 25

        # genre
        if any(g in genres for g in input_genres):
            score += 20

        # semantic
        if m in semantic:
            score += 15

        # collaborative
        if m in collab:
            score += 10

        # popularity
        score += float(row["avg_rating"].values[0]) * 2

        scored.append((m, score))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)

    return [x[0] for x in scored[:top_n]]