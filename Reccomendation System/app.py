import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")
selectvalue = st.selectbox("Select a Movie from the Dropdown", movies_list)

def fetch_poster(movie_id):
    """Fetch movie poster using TMDB API"""
    api_key = "7a13bd86d34c746d61524515206a82c1"  # Replace with your actual key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

    data = response.json()
    
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    """Recommend top 5 similar movies based on similarity scores"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

        recommended_movies = []
        recommended_posters = []
        
        for i in distances[1:6]:  # Get top 5 recommendations
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters
    
    except Exception as e:
        st.error(f"Error in recommendation: {str(e)}")
        return [], []

if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)

    if movie_names:
        cols = st.columns(5)

        for col, name, poster in zip(cols, movie_names, movie_posters):
            with col:
                st.text(name)
                st.image(poster)
    else:
        st.warning("No recommendations found. Please try another movie.")
