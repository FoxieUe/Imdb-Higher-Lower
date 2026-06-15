import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

file_path = os.path.join(BASE_DIR, "data", "imdb_cleaned_movies.csv")


def load_data(path):
    return pd.read_csv(path)


def new_round(df):
    films = df.sample(2)

    film_a = films.iloc[0]
    film_b = films.iloc[1]

    return film_a, film_b


def check(choice, film_a, film_b):
    rating_a = film_a["averageRating"]
    rating_b = film_b["averageRating"]

    return (
        (choice == "A" and rating_a > rating_b)
        or
        (choice == "B" and rating_b > rating_a)
    )


df = load_data(file_path)

df["startYear"] = df["startYear"].astype(int)

score = 0

while True:

    film_a, film_b = new_round(df)

    while (
        film_a["tconst"] == film_b["tconst"]
        or
        film_a["averageRating"] == film_b["averageRating"]
    ):
        film_a, film_b = new_round(df)

    print("=" * 90)
    print(f"{'MOVIE A':^44} | {'MOVIE B':^44}")
    print("=" * 90)

    print(
        f"{film_a['primaryTitle']:^44} | "
        f"{film_b['primaryTitle']:^44}"
    )

    print(
        f"{str(film_a['startYear']):^44} | "
        f"{str(film_b['startYear']):^44}"
    )

    print(
        f"{film_a['genres']:^44} | "
        f"{film_b['genres']:^44}"
    )

    print("=" * 90)

    while True:
        choice = input(
            "Which movie has the higher IMDb rating? (A/B): "
        ).upper()

        if choice in ("A", "B"):
            break

        print("Invalid choice. Enter only A or B.")

    if check(choice, film_a, film_b):

        score += 1

        print("\n✅ Correct answer!")
        print(f"Current score: {score}\n")

    else:

        print("\n❌ Game Over!")

        print(
            f"\nMovie A rating: {film_a['averageRating']}"
        )

        print(
            f"Movie B rating: {film_b['averageRating']}"
        )

        print(
            f"\nFinal score: {score}\n"
        )

        score = 0

        while True:

            restart = input(
                "Play again? (Y/N): "
            ).upper()

            if restart in ("Y", "N"):
                break

            print("Invalid choice.")

        if restart == "Y":
            continue

        break