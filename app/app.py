import streamlit as st
import pandas as pd
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "imdb_cleaned_movies.csv")

API_KEY = "4dc04556"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


def get_poster(imdb_id):
    try:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
        data = requests.get(url, timeout=5).json()

        poster = data.get("Poster")

        if poster and poster != "N/A":
            return poster

    except Exception:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"


def new_round():
    films = df.sample(2)

    st.session_state.film_a = films.iloc[0]
    st.session_state.film_b = films.iloc[1]


def check(choice):
    rating_a = st.session_state.film_a["averageRating"]
    rating_b = st.session_state.film_b["averageRating"]

    correct = (
        (choice == "A" and rating_a > rating_b)
        or
        (choice == "B" and rating_b > rating_a)
    )

    if correct:
        st.session_state.score += 1
        new_round()
    else:
        st.session_state.game_over = True


st.set_page_config(
    page_title="IMDb Higher / Lower",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    max-width: 900px;
    margin: auto;
    padding-top: 2rem;
}

h1, h2, h3 {
    text-align: center;
}

div[data-testid="column"] {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

df = load_data(file_path)

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.game_over = False

    films = df.sample(2)

    st.session_state.film_a = films.iloc[0]
    st.session_state.film_b = films.iloc[1]

st.title(" IMDb Higher / Lower")
st.markdown(
    "<p style='text-align:center;'>Choose the movie with the higher IMDb rating.</p>",
    unsafe_allow_html=True
)

st.divider()

film_a = st.session_state.film_a
film_b = st.session_state.film_b

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown("## Movie A")

    st.image(
        get_poster(film_a["tconst"]),
        width = 275
    )

    st.markdown(f"""
    <div style="text-align:center;">
        <h3>{film_a['primaryTitle']}</h3>
        <p>{film_a['startYear']} • {film_a['genres']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Choose A",
        use_container_width=True,
        disabled=st.session_state.game_over
    ):
        check("A")
        st.rerun()

with col2:

    st.markdown("## Movie B")

    st.image(
        get_poster(film_b["tconst"]),
        width = 275
    )

    st.markdown(f"""
    <div style="text-align:center;">
        <h3>{film_b['primaryTitle']}</h3>
        <p>{film_b['startYear']} • {film_b['genres']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Choose B",
        use_container_width=True,
        disabled=st.session_state.game_over
    ):
        check("B")
        st.rerun()

if st.session_state.game_over:

    st.divider()

    st.error(
        f"Game Over!\n\n"
        f"Final Score: {st.session_state.score}\n\n"
        f"Movie A Rating: {film_a['averageRating']}\n"
        f"Movie B Rating: {film_b['averageRating']}"
    )

    if st.button(
        "🔄 Play Again",
        use_container_width=True
    ):
        st.session_state.score = 0
        st.session_state.game_over = False

        new_round()

        st.rerun()