import pickle
import streamlit as st
import requests
import time
from huggingface_hub import hf_hub_download

# ===============================
# CONFIG
# ===============================
# Use Streamlit secrets for API key (set it in Streamlit Cloud/Vercel dashboard)
API_KEY = st.secrets["API_KEY"]

# Hugging Face repo where model files are stored
REPO_ID = "Sakshi2064/movie-recommender-model"  # 🔴 replace with your repo name

# ===============================
# HELPER FUNCTIONS
# ===============================
def fetch_poster(movie_id: int) -> str:
    """Fetch movie poster from TMDB API with retries and fallback."""
    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key={API_KEY}&language=en-US"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
            else:
                return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie: str):
    """Return top 5 recommended movie names and posters."""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = int(movies.iloc[i[0]].movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# ===============================
# STREAMLIT APP
# ===============================
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #e50914;
        font-size: 46px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    /* Dropdown label */
    .stSelectbox label {
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: 600 !important;
    }
    /* Dropdown text */
    div[data-baseweb="select"] span {
        font-size: 20px !important;
        color: #000000 !important;
    }
    /* Button styling */
    .stButton>button {
        background-color: #e50914;
        color: white;
        border: none;
        padding: 14px 32px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #ff1e1e;
        transform: scale(1.05);
        box-shadow: 0px 0px 12px #e50914;
    }
    .stButton>button:active {
        transform: scale(0.94); /* click effect */
        background-color: #cc0812;
    }
    /* Movie cards */
    .movie-card {
        background: #1c1c1c;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .movie-card:hover {
        transform: scale(1.06);
        box-shadow: 0px 0px 15px rgba(229, 9, 20, 0.6);
    }
    .movie-card img {
        border-radius: 10px;
        width: 100%;
        height: auto;
    }
    .movie-title {
        color: white;
        font-size: 18px;
        margin-top: 10px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 class='main-title'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

# ===============================
# LOAD MODEL FILES
# ===============================
try:
    movie_list_path = hf_hub_download(repo_id=REPO_ID, filename="movie_list.pkl")
    similarity_path = hf_hub_download(repo_id=REPO_ID, filename="similarity.pkl")

    movies = pickle.load(open(movie_list_path, "rb"))
    similarity = pickle.load(open(similarity_path, "rb"))
except Exception as e:
    st.error(f"⚠️ Could not load model files from Hugging Face Hub: {e}")
    st.stop()

# ===============================
# UI
# ===============================
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

if st.button('✨ Show Recommendations'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" alt="{name}">
                    <div class="movie-title">{name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
