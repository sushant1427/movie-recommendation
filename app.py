import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=226a7b2db1de7f25c374b29a4fd231c1&language=en-US".format(movie_id))
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None
    except Exception as e:
        st.error("Error fetching movie poster: {}".format(str(e)))
        return None

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distance = similarity[movie_index]
        movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = []
        recommended_movie_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].get('movie_id')
            if movie_id:
                poster_url = fetch_poster(movie_id)
                if poster_url:
                    recommended_movie_posters.append(poster_url)
                    recommended_movies.append(movies.iloc[i[0]]['title'])
        return recommended_movies, recommended_movie_posters
    except Exception as e:
        st.error("Error recommending movies: {}".format(str(e)))
        return [], []

movie_dict = pickle.load(open("movies_dict.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open("similarty.pkl", 'rb'))

st.title("Movie Recommendation System")
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    if names and posters:
        for name, poster in zip(names, posters):
            st.header(name)
            st.image(poster,width=200)
    else:
        st.warning("No recommendations found.")
