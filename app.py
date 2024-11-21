import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:  # Check if the request was successful
        data = response.json()
        if 'poster_path' in data and data['poster_path'] is not None:
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Placeholder if poster is missing


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)  # Append movie title
        recommended_movie_posters.append(fetch_poster(movie_id))  # Append poster

    return recommended_movies, recommended_movie_posters


# Load pre-processed data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Create 5 columns for displaying recommendations

    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
