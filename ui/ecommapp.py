import streamlit as st
import requests
import jwt
import pandas as pd

# Base API URL
BASE_URL = "http://127.0.0.1:8000"
SECRET_KEY = "your_secret_key"  # Replace with the actual secret key
ALGORITHM = "HS256"

# Initialize session state variables if they don't exist
if "token" not in st.session_state:
    st.session_state["token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None


# Authenticate Function
def authenticate(username, password):
    response = requests.post(
        f"{BASE_URL}/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )
    # print(f"response :{response}")
    print(f"response :{response.json()}")
    
    if response.status_code != 200:
        return False
    
    reply = response.json()
    token = reply.get("access_token")
    # decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_role = reply.get("roles", "unknown")
    st.session_state["username"] = username
    st.session_state["role"] = user_role
    st.session_state["token"] = token

    return True


def login_section():
    # Check if already logged in
    if st.session_state["token"]:
        st.write(f"### Logged in as: {st.session_state['username']}")
        st.write(f"**Role:** {st.session_state['role']}")
        if st.button("Logout"):
            st.session_state["token"] = None
            st.session_state["username"] = None
            st.session_state["role"] = None
            st.success("Logged out successfully!")
            st.rerun()  # Immediately re-run the app
    else:
        # Login form
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if authenticate(username, password):
                # Set query parameters using st.experimental_set_query_params (updated to st.query_params)
                st.session_state["logged_in"] = True  # Manage state directly
                st.success("Login successful!")
            else:
                st.error("Authentication failed")
            st.rerun()  # Immediately re-run the app


# CRUD Operation Functions
def create_movie(token, title, director, genre, year):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": title, "director": director, "genre": genre, "year": year}
    response = requests.post(f"{BASE_URL}/movies/", json=payload, headers=headers)
    return response

def fetch_all_movies(token):
    """
    Fetch all movies from the backend and return as a DataFrame.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/movies", headers=headers)
    
    if response.status_code == 200:
        movies = response.json()
        # Convert the JSON response to a DataFrame
        return pd.DataFrame(movies)
    else:
        st.error("Failed to fetch movies")
        return pd.DataFrame()  # Return an empty DataFrame on failure

def list_movies_section():
    """
    Display all movies in a tabular format.
    """
    st.subheader("List of Movies")

    # Fetch movies
    if "token" in st.session_state and st.session_state["token"]:
        movies_df = fetch_all_movies(st.session_state["token"])

        if not movies_df.empty:
            st.dataframe(movies_df)  # Display the DataFrame as a table
        else:
            st.warning("No movies found.")
    else:
        st.error("Please log in to view the list of movies.")

def read_movie(token, movie_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    return response


def update_movie(token, movie_id, title, director, genre, year):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": title, "director": director, "genre": genre, "year": year}
    response = requests.put(f"{BASE_URL}/movies/{movie_id}", json=payload, headers=headers)
    return response


def delete_movie(token, movie_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    return response


# Movie Management Sections
def create_movie_section():
    st.subheader("Create Movie")
    title = st.text_input("Title")
    director = st.text_input("Director")
    genre = st.text_input("Genre")
    year = st.number_input("Year", step=1)
    if st.button("Create Movie"):
        response = create_movie(st.session_state["token"], title, director, genre, year)
        if response.status_code == 200:
            st.success("Movie created successfully")
        else:
            st.error(response.json().get("detail", "Error creating movie"))


def read_movie_section():
    st.subheader("Read Movie")
    movie_id = st.number_input("Movie ID", step=1)
    if st.button("Fetch Movie"):
        response = read_movie(st.session_state["token"], movie_id)
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error fetching movie"))


def update_movie_section():
    st.subheader("Update Movie")
    movie_id = st.number_input("Movie ID to Update", step=1, key="update_id")
    title = st.text_input("New Title", key="update_title")
    director = st.text_input("New Director", key="update_director")
    genre = st.text_input("New Genre", key="update_genre")
    year = st.number_input("New Year", step=1, key="update_year")
    if st.button("Update Movie"):
        response = update_movie(st.session_state["token"], movie_id, title, director, genre, year)
        if response.status_code == 200:
            st.success("Movie updated successfully")
        else:
            st.error(response.json().get("detail", "Error updating movie"))


def delete_movie_section():
    st.subheader("Delete Movie")
    movie_id = st.number_input("Movie ID to Delete", step=1, key="delete_id")
    if st.button("Delete Movie"):
        response = delete_movie(st.session_state["token"], movie_id)
        if response.status_code == 200:
            st.success("Movie deleted successfully")
        else:
            st.error(response.json().get("detail", "Error deleting movie"))


# Main Application
def main():
    st.title("Movie Management System")

    # Sidebar for Login
    with st.sidebar:
        login_section()

    # Main Content
    if st.session_state["token"]:
        st.header("Manage Movies")
        tabs = st.tabs(["Create", "Read", "Update", "Delete", "List"])

        with tabs[0]:
            create_movie_section()

        with tabs[1]:
            read_movie_section()

        with tabs[2]:
            update_movie_section()

        with tabs[3]:
            delete_movie_section()
    
        with tabs[4]:
            list_movies_section()  # List movies tab
    else:
        st.warning("Please log in to access the application.")


if __name__ == "__main__":
    main()
