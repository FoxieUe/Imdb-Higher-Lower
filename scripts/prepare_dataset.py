import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

basics_path = os.path.join(
    BASE_DIR,
    "data",
    "title.basics.tsv.gz"
)

ratings_path = os.path.join(
    BASE_DIR,
    "data",
    "title.ratings.tsv.gz"
)

output_path = os.path.join(
    BASE_DIR,
    "data",
    "imdb_cleaned_movies.csv"
)

stats = {}



movies = pd.read_csv(
    basics_path,
    sep="\t",
    compression="gzip",
    na_values="\\N",
    keep_default_na=False,
    low_memory=False
)

stats["Raw title.basics records"] = len(movies)



movies = movies[
    movies["titleType"].isin(["movie", "tvMovie"])
]

stats["Movies and TV movies"] = len(movies)



movies["startYear"] = pd.to_numeric(
    movies["startYear"],
    errors="coerce"
)

stats["Missing release year"] = (
    movies["startYear"].isna().sum()
)

movies = movies[
    movies["startYear"] >= 2000
]

stats["Movies released after 2000"] = len(movies)


movies["runtimeMinutes"] = pd.to_numeric(
    movies["runtimeMinutes"],
    errors="coerce"
)

stats["Missing runtime"] = (
    (movies["runtimeMinutes"].isna())
    |
    (movies["runtimeMinutes"] <= 0)
).sum()

movies = movies[
    movies["runtimeMinutes"] > 0
]

stats["Valid runtime movies"] = len(movies)


ratings = pd.read_csv(
    ratings_path,
    sep="\t",
    compression="gzip",
    na_values="\\N",
    keep_default_na=False,
    low_memory=False
)

movies = pd.merge(
    movies,
    ratings,
    on="tconst",
    how="left"
)

stats["Missing rating"] = (
    movies["averageRating"].isna().sum()
)

movies = movies[
    movies["averageRating"].notna()
]

movies = movies[
    movies["numVotes"] >= 50000
]

stats["Movies with 50k+ votes"] = len(movies)


print("\nIMDb Dataset Preparation\n")
print("-" * 60)

for label, value in stats.items():
    print(f"{label:<35} {value:>10}")

print("-" * 60)
print(f"Final dataset size{'':<16} {len(movies):>10}")


movies["startYear"] = (
    movies["startYear"].astype(int)
)

movies.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset exported successfully.")