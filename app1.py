import pickle
import streamlit as st
import requests


# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Function to fetch details of a selected movie
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    details = {
        'title': data.get('title', 'N/A'),
        'overview': data.get('overview', 'N/A'),
        'release_date': data.get('release_date', 'N/A'),
        'rating': data.get('vote_average', 'N/A'),
        'poster': f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}"
    }
    return details


# Function to recommend movies based on the selected movie
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit App
st.markdown("<h1 style='text-align: center;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# Load movies and similarity data
movies = pickle.load(open('movies1.pkl', 'rb'))
similarity = pickle.load(open('similarity1.pkl', 'rb'))

# Movie Selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Screen layout with two columns
left_col, right_col = st.columns([1, 2])  # Left column smaller for details, right column larger for recommendations

# Show selected movie details on the left side
if selected_movie:
    selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    movie_details = fetch_movie_details(selected_movie_id)

    with left_col:
        st.subheader("Selected Movie Details")
        st.image(movie_details['poster'], width=150)  # Smaller poster size
        st.write(f"**Title**: {movie_details['title']}")
        st.write(f"**Overview**: {movie_details['overview']}")  # Show full overview
        st.write(f"**Release Date**: {movie_details['release_date']}")
        st.write(f"**Rating**: {movie_details['rating']}")

# Show recommendation button and recommended movies on the right side
with right_col:
    st.subheader("Recommendations")
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        # Display recommended movies in a row with larger images
        cols = st.columns(5)  # Create 5 columns for 5 recommended movies
        for idx, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
            with cols[idx]:
                st.image(poster, use_column_width=True)  # Make images larger
                st.markdown(f"**{name}**", unsafe_allow_html=True)  # Bold title for emphasis
