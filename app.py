import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    return poster_path

movie_list_file = open("../output/movies_list.pkl","rb")
movies = pickle.load(movie_list_file)
similarity = pickle.load(open("../output/similarity.pkl","rb"))
movie_list = movies['title'].values

st.header("Movie Recommender System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue = st.selectbox("Select Movie from dropdown",movie_list)



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommended_movies = []
    recommended_posters = []
    for i in distance[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies.iloc[i[0]].id))

    return recommended_movies,recommended_posters

if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.image(movie_posters[0])
        st.text(movie_names[0])
    with col2:
        st.image(movie_posters[1])
        st.text(movie_names[1])
    with col3:
        st.image(movie_posters[2])
        st.text(movie_names[2])
    with col4:
        st.image(movie_posters[3])
        st.text(movie_names[3])
    with col5:
        st.image(movie_posters[4])
        st.text(movie_names[4])

