# 🎬 Movie Recommender AI
## 🚀 AI-powered movie recommendation system that suggests movies based on user preferences using a hybrid approach combining:


### 🤖 Semantic AI (NLP embeddings)
🎯 Collaborative Filtering
⭐ Popularity-based ranking
🔥 Features
🎬 Smart movie recommendations (Netflix-style logic)
🔍 Flexible search (no exact spelling needed)
🧠 Meaning-based suggestions (not just keywords)
🎯 Franchise + genre-aware ranking
🎥 Movie posters, ratings, and descriptions
🎭 Sidebar with all available genres
⚡ Fast performance with caching
🌐 Interactive UI built using Streamlit


### 🧠 How It Works
This system uses a hybrid recommendation approach:
#### 1. Semantic AI (NLP)
Uses SentenceTransformer to understand movie meaning
Recommends movies based on context (e.g., superhero vibe)
#### 2. Collaborative Filtering
Finds similar movies based on user rating patterns
#### 3. Ranking System
Movies are ranked using:
Franchise similarity (same series)
Keyword match
Genre overlap
Semantic similarity
Collaborative similarity
Popularity (average rating)

### 🛠 Tech Stack
Python
Streamlit
Pandas / NumPy
Scikit-learn
Sentence Transformers (MiniLM)
OMDb API

### 📁 Project Structure
movie-recommender-ai/
│
├── app.py               # Streamlit frontend
├── recommender.py      # ML + AI logic
├── movies.csv
├── ratings.csv
├── links.csv
├── embeddings.npy      # Cached embeddings (for speed)
├── requirements.txt
└── README.md


### ⚙️ Setup & Run Locally
#### 1. Clone repo
git clone https://github.com/your-username/movie-recommender-ai.git
cd movie-recommender-ai
#### 2. Install dependencies
pip install -r requirements.txt
#### 3. Add OMDb API Key
Create a .env file:
OMDB_API_KEY=your_api_key_here
#### 4. Run app
streamlit run app.py

### 🌐 Live Demo

👉 (Add your deployed Streamlit link here)

### 📸 Screenshots

(Add your project screenshots here)

🚀 Future Improvements
👤 User-based personalization
❤️ Watch history & recommendations
📊 Trending / popular movies section
🎨 Advanced UI (Netflix-style cards)
☁️ Deployment with database support

### 🙌 Author
Utsav Ratpiya

💼 Aspiring AI/ML Engineer & Entrepreneur
🔗 LinkedIn: https://www.linkedin.com/in/utsav-ratpiya-2b9470284/

⭐ If you like this project
Give it a ⭐ on GitHub — it helps a lot!
