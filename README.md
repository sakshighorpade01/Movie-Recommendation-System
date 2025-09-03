# 🎬 Movie Recommendation System

A **Machine Learning-based Movie Recommendation System** that suggests movies similar to your favorites.  
The app is deployed on **Streamlit Cloud** and uses **The Movie Database (TMDB) API** to fetch real movie posters.  

👉 **Live Demo**: [Movie Recommender App](https://movie-recommendation-system-f7eebe7g8uwdgfy2auxxje.streamlit.app/)

---

## 🚀 Features
- 🔍 Search and select a movie from the dropdown  
- 🎥 Get **Top 5 similar movie recommendations**  
- 🖼️ Posters fetched dynamically using TMDB API  
- 🌐 Deployed on Streamlit Cloud — accessible to everyone  

---

## 🛠️ Tech Stack
- **Python**
- **Machine Learning (Scikit-learn, Pandas, Numpy)**
- **Streamlit** → for UI and deployment
- **Hugging Face Hub** → hosting `.pkl` model files
- **TMDB API** → for movie posters  

---

## 📂 Project Structure

📦 Movie-Recommendation-System
├── app.py # Streamlit app
├── requirements.txt # Dependencies
├── notebook.ipynb # ML model training (optional, for reference)
└── README.md # Documentation


## ⚡ How It Works
1. Dataset is preprocessed and feature vectors are created.  
2. The ML model computes **cosine similarity** between movies.  
3. When a user selects a movie, the system finds the **5 most similar movies**.  
4. Posters are fetched from TMDB API for a better visual experience.  

---


