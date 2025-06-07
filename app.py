import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile
import pickle

def fetch(movie_title):
    api_key = "e0ba1fd0"  # Replace with your actual key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Request failed:", response.status_code)
            return "https://via.placeholder.com/500x750?text=Error"
        
        data = response.json()
        
        if data.get("Response") == "False":
            print("OMDb error:", data.get("Error"))
            return "https://via.placeholder.com/500x750?text=Not+Found"
        
        return data.get("Poster", "https://via.placeholder.com/500x750?text=No+Image")

    except Exception as e:
        print("Exception:", e)
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    movies_recommended = []
    recommend_movie_posters=[]
    for i in movies:
        movie_id = i[0]
        movie_title = movies_df.iloc[movie_id].title
        
        movies_recommended.append(movies_df.iloc[i[0]].title)
        recommend_movie_posters.append(fetch(movie_title))

    return movies_recommended,recommend_movie_posters

movies_df = pickle.load(open('movies.pkl', 'rb'))  # Load full DataFrame
movies_list = movies_df['title'].values  # Just for selectbox display

with zipfile.ZipFile("similarity.zip", "r") as zip_ref:
    with zip_ref.open("similarity.pkl") as f:
        similarity = pickle.load(f)

st.title('Movie Recommender System')
selected_movie_name = st.selectbox("Select a movie", movies_list)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5  = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    
    with col4:
        st.text(names[3])
        st.image(posters[3])
    
    with col5:
        st.text(names[4])
        st.image(posters[4])