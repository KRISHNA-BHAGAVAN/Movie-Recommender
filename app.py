import pickle
import streamlit as st
import requests
import gdown  
import os

# Google Drive file ID of similarity.pkl
FILE_ID = "1ur7P1wNZlGxxzuh1rtPq1ExovaFthQGi"
OUTPUT_PATH = "similarity.pkl"

# Function to download similarity.pkl from Google Driv
@st.cache_data
def load_similarity():
    if not os.path.exists(OUTPUT_PATH):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, OUTPUT_PATH, quiet=False)
    return pickle.load(open(OUTPUT_PATH, "rb"))

similarity = load_similarity()

movies = pickle.load(open('movie_list.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8be11877c759e70a06a0c8028c07257d&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(poster)

    return recommended_movie_names, recommended_movie_posters

st.header('🎬 Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Type or select a movie:", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)




