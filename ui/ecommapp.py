import streamlit as st
import requests
import pandas as pd
from streamlit_cookies_manager import EncryptedCookieManager

# Cookie manager for persistent state
cookies = EncryptedCookieManager(prefix="movieapp_", password="your_secret_key")
if not cookies.ready():
    st.stop()

# Base API URL
BASE_URL = "http://127.0.0.1:8000"

# Initialize session state
def initialize_session():
    if "token" not in st.session_state:
        st.session_state["token"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False


# Authentication and Authorization
def authenticate_user(username, password):
    """Authenticate user and store session details in cookies."""
    response = requests.post(
        f"{BASE_URL}/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )
    if response.status_code != 200:
        return False
    data = response.json()
    cookies["token"] = data.get("access_token")
    cookies["username"] = username
    cookies["role"] = data.get("roles", "unknown")
    cookies.save()
    return True


def is_logged_in():
    """Check if the user is logged in."""
    return "token" in cookies and cookies.get("token")


def logout_user():
    """Clear session cookies."""
    cookies.delete("token")
    cookies.delete("username")
    cookies.delete("role")
    cookies.save()
    st.rerun()
    # st.experimental_rerun()


# API Helpers
def make_authorized_request(method, endpoint, token, **kwargs):
    """Helper to make authorized API requests."""
    print("token_authorise", token)
    headers = {"Authorization": f"Bearer {token}"}
    print("headers", headers)
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, headers=headers, **kwargs)
    return response


def fetch_movies():
    """Fetch all movies from the API."""
    token = cookies.get("token")
    response = make_authorized_request("GET", "/movies", token)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    st.error("Failed to fetch movies")
    return pd.DataFrame()


def create_movie(payload):
    """Create a new movie."""
    token = cookies.get("token")
    return make_authorized_request("POST", "/movies/", token, json=payload)


def update_movie(movie_id, payload):
    """Update an existing movie."""
    token = cookies.get("token")
    return make_authorized_request("PUT", f"/movies/{movie_id}", token, json=payload)


def delete_movie(movie_id):
    """Delete a movie."""
    token = cookies.get("token")
    return make_authorized_request("DELETE", f"/movies/{movie_id}", token)


def render_logged_in_section():
    """Render the section for logged-in users."""
    st.write(f"### Logged in as: {cookies.get('username')}")
    st.write(f"**Role:** {cookies.get('role')}")
    if st.button("Logout"):
        logout_user()


def render_login_form():
    """Render the login form for users to input credentials."""
    st.header("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        handle_login(username, password)


def handle_login(username, password):
    """Handle the login process."""
    if authenticate_user(username, password):
        st.success("Login successful!")
        st.rerun()
        # st.experimental_rerun()
    else:
        st.error("Authentication failed")


def login_section():
    """Render the login/logout section by deciding which state to display."""
    if is_logged_in():
        render_logged_in_section()
    else:
        render_login_form()


def movie_management_tabs():
    """Render the movie management tabs."""
    tabs = st.tabs(["Create", "Read", "Update", "Delete", "List"])

    with tabs[0]:
        create_movie_ui()

    with tabs[1]:
        read_movie_ui()

    with tabs[2]:
        update_movie_ui()

    with tabs[3]:
        delete_movie_ui()

    with tabs[4]:
        list_movies_ui()


def create_movie_ui():
    """Render UI for creating a movie."""
    st.subheader("Create Movie")
    title = st.text_input("Title")
    director = st.text_input("Director")
    genre = st.text_input("Genre")
    year = st.number_input("Year", step=1)
    if st.button("Create Movie"):
        payload = {"title": title, "director": director, "genre": genre, "year": year}
        response = create_movie(payload)
        if response.status_code == 200:
            st.success("Movie created successfully")
        else:
            st.error(response.json().get("detail", "Error creating movie"))


def read_movie_ui():
    """Render UI for reading a movie."""
    st.subheader("Read Movie")
    movie_id = st.number_input("Movie ID", step=1)
    if st.button("Fetch Movie"):
        token = cookies.get("token")
        print("token_read", token)
        response = make_authorized_request("GET", f"/movies/{movie_id}", token)
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error fetching movie"))


def update_movie_ui():
    """Render UI for updating a movie."""
    st.subheader("Update Movie")
    movie_id = st.number_input("Movie ID to Update", step=1, key="update_id")
    title = st.text_input("New Title", key="update_title")
    director = st.text_input("New Director", key="update_director")
    genre = st.text_input("New Genre", key="update_genre")
    year = st.number_input("New Year", step=1, key="update_year")
    if st.button("Update Movie"):
        payload = {"title": title, "director": director, "genre": genre, "year": year}
        response = update_movie(movie_id, payload)
        if response.status_code == 200:
            st.success("Movie updated successfully")
        else:
            st.error(response.json().get("detail", "Error updating movie"))


def delete_movie_ui():
    """Render UI for deleting a movie."""
    st.subheader("Delete Movie")
    movie_id = st.number_input("Movie ID to Delete", step=1, key="delete_id")
    if st.button("Delete Movie"):
        response = delete_movie(movie_id)
        if response.status_code == 200:
            st.success("Movie deleted successfully")
        else:
            st.error(response.json().get("detail", "Error deleting movie"))


def list_movies_ui():
    """Render UI for listing all movies."""
    st.subheader("List of Movies")
    if is_logged_in():
        movies_df = fetch_movies()
        if not movies_df.empty:
            st.dataframe(movies_df)  # Display movies as a table
        else:
            st.warning("No movies found.")
    else:
        st.error("Please log in to view the list of movies.")


# Main Application
def main():
    """Main function to run the application."""
    initialize_session()
    st.title("Movie Management System")

    # Sidebar for Login
    with st.sidebar:
        login_section()

    # Main Content
    if is_logged_in():
        st.header("Manage Movies")
        movie_management_tabs()
    else:
        st.warning("Please log in to access the application.")


if __name__ == "__main__":
    main()
