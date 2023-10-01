import streamlit as st
import pickle
import requests
from pathlib import Path
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

# --- USER AUTHENTICATION ---
names = ["Sandeep Pratap", "Pratyaya Prakash", "Govind Pandey", "Abhinav Kumar"]
usernames = ["sandeep007", "pratyaya057", "govind047", "abhinav008"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "movies_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main") # main body or side-bar

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=4dcaab1bf38b4ba42fd052fa044d92b8".format(movie_id)
        data=requests.get(url)
        data=data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
        return full_path

    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list=movies['title'].values

    # logout

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    # st.set_page_config(page_title=f"Welcome {name}")

    st.title("Movie Recommender System")

    # import streamlit.components.v1 as components

    selectvalue=st.selectbox("Select movie from dropdown", movies_list)

    def recommend(movie):
        index=movies[movies['title']==movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
        recommend_movie=[]
        recommend_poster=[]
        recommend_genres=[]
        recommend_tagline=[]
        recommend_overview=[]
        recommend_cast=[]
        recommend_director=[]
    
        for i in distance[1:6]:
            movies_id=movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movies_id))
            recommend_genres.append(movies.iloc[i[0]].genres)
            recommend_tagline.append(movies.iloc[i[0]].tagline)
            recommend_overview.append(movies.iloc[i[0]].overview)
            recommend_cast.append(movies.iloc[i[0]].cast)
            recommend_director.append(movies.iloc[i[0]].director)

        return recommend_movie, recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director



    if st.button("Show Recommendation"):
        movie_name, movie_poster, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)
        col1,col2,col3,col4,col5=st.columns(5)

        for i in range(5):
            if i == 0:
                col = col1
            elif i == 1:
                col = col2
            elif i == 2:
                col = col3
            elif i == 3:
                col = col4
            else:
                col = col5

            with col:    
                st.markdown(f"**{movie_name[i]}**")
                st.image(movie_poster[i], use_column_width=True)
                
                with st.expander(f"Movie Description"):
                    st.markdown("**Tagline:** "+f"{movie_tagline[i]}")
                    st.markdown("**Genres:** "+f"{movie_genres[i]}")
                    st.markdown("**Overview:** "+f"{movie_overview[i]}")
                    st.markdown("**Cast:** "+f"{movie_cast[i]}")
                    st.markdown("**Director:** "+f"{movie_director[i]}")

    # Display 5 popular movies on the home screen in one row with 5 columns
    st.header("Popular Movies")
    popular_movies = movies.sort_values(by='popularity', ascending=False).head(5)
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, movie in popular_movies.iterrows():
        movie_name = movie['title']
        movie_poster = fetch_poster(movie['id'])
        
        with col1 if i % 5 == 0 else col2 if i % 5 == 1 else col3 if i % 5 == 2 else col4 if i % 5 == 3 else col5:
            st.markdown(f"**{movie_name}**")
            st.image(movie_poster, use_column_width=True)
            
            with st.expander(f"Movie Description"):
                st.markdown("**Tagline:** "+f"{movie['tagline']}")
                st.markdown("**Genres:** "+f"{movie['genres']}")
                st.markdown("**Overview:** "+f"{movie['overview']}")
                st.markdown("**Cast:** "+f"{movie['cast']}")
                st.markdown("**Director:** "+f"{movie['director']}")


    # Create a dictionary where keys are genres and values are lists of movie titles in that genre
    genre_movies = {}

    for index, row in movies.iterrows():
        genres = row['genres']
        if isinstance(genres, str):  # Check if 'genres' is a valid string
            genres = genres.split(' ')
            for genre in genres:
                if genre in genre_movies:
                    genre_movies[genre].append(row['title'])
                else:
                    genre_movies[genre] = [row['title']]

    # Select a genre from the list
    selected_genre = st.selectbox("Select a genre", list(genre_movies.keys()))

    # Add a button to show the results
    show_results = st.button("Show Movies")

    if show_results:

        # Display the most popular movies in the selected genre
        st.header(f"Popular Movies in {selected_genre}")
        popular_movies_in_genre = genre_movies.get(selected_genre, [])

        if popular_movies_in_genre:
            columns = st.columns(5)
            
            for i, movie_name in enumerate(popular_movies_in_genre[:5]):
                movie = movies[movies['title'] == movie_name].iloc[0]
                movie_poster = fetch_poster(movie['id'])

                with columns[i]:
                    st.markdown(f"**{movie_name}**")
                    st.image(movie_poster)

                    with st.expander(f"Movie Description"):
                        st.markdown("**Tagline:** " + f"{movie['tagline']}")
                        st.markdown("**Genres:** " + f"{movie['genres']}")
                        st.markdown("**Overview:** " + f"{movie['overview']}")
                        st.markdown("**Cast:** " + f"{movie['cast']}")
                        st.markdown("**Director:** " + f"{movie['director']}")
        else:
            st.warning(f"No popular movies found in {selected_genre} genre.")



