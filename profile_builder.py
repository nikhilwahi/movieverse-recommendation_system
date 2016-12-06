#!flask/bin/python


from movielens import *
from sklearn.cluster import KMeans

import numpy as np
import pickle
import random
import sys
import time
import json
import traceback
from flask import jsonify
import MySQLdb as MySQL

import os
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"


counter = 943
user = []
item = []

d = Dataset()
d.load_users(dir_path + "data/u.user", user)
d.load_items(dir_path + "data/u.item", item)

input_movies = []


def supply_sample_movies():
    random_movies = random.sample(item, 10)
    input_movies = random_movies

    movie_names = []
    for movie in input_movies:
        movie_names.append(movie.title)
    return movie_names


def return_preferred_genres(user_ratings, age, gender, occupation, user_id):
    n_users = len(user)
    n_items = len(item)

    utility_matrix = pickle.load(open(dir_path + "utility_matrix.pkl", "rb"))

    # Find the average rating for each user and stores it in the user's object
    for i in range(0, n_users):
        x = utility_matrix[i]
        user[i].avg_r = sum(a for a in x if a > 0) / sum(a > 0 for a in x)

    # Perform clustering on items
    movie_genre = []
    for movie in item:
        movie_genre.append([movie.unknown, movie.action, movie.adventure, movie.animation, movie.childrens, movie.comedy, movie.crime, movie.documentary, movie.drama, movie.fantasy, movie.film_noir, movie.horror,
                            movie.musical, movie.mystery, movie.romance, movie.sci_fi, movie.thriller, movie.war, movie.western])

    movie_genre = np.array(movie_genre)
    cluster = KMeans(n_clusters=19)
    cluster.fit_predict(movie_genre)

    global input_movies
    movies = input_movies

    new_user = np.zeros(19)

    for i, movie in enumerate(movies):
        a = user_ratings[i]
        if new_user[cluster.labels_[movie.id - 1]] != 0:
            new_user[cluster.labels_[movie.id - 1]
                     ] = (new_user[cluster.labels_[movie.id - 1]] + a) / 2
        else:
            new_user[cluster.labels_[movie.id - 1]] = a

    utility_new = np.vstack((utility_matrix, new_user))

    user.append(User(944, age, gender, occupation, 110018))
    #user.append(User(944, age, gender, occupation, 100000+user_id))

    pcs_matrix = np.zeros(n_users)

    print "Finding users which have similar preferences."
    for i in range(0, n_users + 1):
        if i != 943:
            pcs_matrix[i] = pcs(944, i + 1, utility_new)

    user_index = []
    for i in user:
        user_index.append(i.id - 1)

    user_index = user_index[:943]
    user_index = np.array(user_index)

    top_5 = [x for (y, x) in sorted(zip(pcs_matrix, user_index),
                                    key=lambda pair: pair[0], reverse=True)]
    top_5 = top_5[:5]

    top_5_genre = []


    for i in range(0, 5):
        maxi = 0
        maxe = 0
        for j in range(0, 19):
            if maxe < utility_matrix[top_5[i]][j]:
                maxe = utility_matrix[top_5[i]][j]
                maxi = j
        top_5_genre.append(maxi)

    preferred_genres_ids = []
    preferred_genres_name = []

    for i in top_5_genre:
        if i == 0:
            preferred_genres_ids.append(28)
            preferred_genres_name.append('Lifestyle')
        elif i == 1:
            preferred_genres_ids.append(25)
            preferred_genres_name.append('Action')
        elif i == 2:
            preferred_genres_ids.append(18)
            preferred_genres_name.append('Adventure')
        elif i == 3:
            preferred_genres_ids.append(24)
            preferred_genres_name.append('Animation')
        elif i == 4:
            preferred_genres_ids.append(16)
            preferred_genres_name.append('Family')
        elif i == 5:
            preferred_genres_ids.append(7)
            preferred_genres_name.append('Comedy')
        elif i == 6:
            preferred_genres_ids.append(10)
            preferred_genres_name.append('Crime')
        elif i == 7:
            preferred_genres_ids.append(1)
            preferred_genres_name.append('Documentary')
        elif i == 8:
            preferred_genres_ids.append(6)
            preferred_genres_name.append('Drama')
        elif i == 9:
            preferred_genres_ids.append(23)
            preferred_genres_name.append('Fantasy')
        elif i == 10:
            preferred_genres_ids.append(29)
            preferred_genres_name.append('Film_Noir')
        elif i == 11:
            preferred_genres_ids.append(3)
            preferred_genres_name.append('Horror')
        elif i == 12:
            preferred_genres_ids.append(9)
            preferred_genres_name.append('Musical')
        elif i == 13:
            preferred_genres_ids.append(11)
            preferred_genres_name.append('Mystery')
        elif i == 14:
            preferred_genres_ids.append(15)
            preferred_genres_name.append('Romance')
        elif i == 15:
            preferred_genres_ids.append(14)
            preferred_genres_name.append('Sci-Fi')
        elif i == 16:
            preferred_genres_ids.append(5)
            preferred_genres_name.append('Thriller')
        elif i == 17:
            preferred_genres_ids.append(22)
            preferred_genres_name.append('War')
        else:
            preferred_genres_ids.append(27)
            preferred_genres_name.append('Western')

    try:
        conn = MySQL.connect(host="127.0.0.1", user="root", passwd="cs411fa2016", db="imdb")
        cursor = conn.cursor()
        for genre in preferred_genres_ids:
            query = "INSERT INTO UserGenre(UserID,GenreID) VALUES(%d,%d)" % (user_id, genre)
            try:
                x = cursor.execute(query)
                conn.commit()
            except MySQL.Error as e:
                conn.rollback()
                raise
                return False, None, "SQL connection error"
    except MySQL.Error as e:
        traceback.print_exc()
        print "SQL Connection Error"

    return list(set(preferred_genres_name))


# Find the Pearson Correlation Similarity Measure between two users
def pcs(x, y, ut):
    num = 0
    den1 = 0
    den2 = 0
    A = ut[x - 1]
    B = ut[y - 1]
    num = sum((a - user[x - 1].avg_r) * (b - user[y - 1].avg_r)
              for a, b in zip(A, B) if a > 0 and b > 0)
    den1 = sum((a - user[x - 1].avg_r) ** 2 for a in A if a > 0)
    den2 = sum((b - user[y - 1].avg_r) ** 2 for b in B if b > 0)
    den = (den1 ** 0.5) * (den2 ** 0.5)
    if den == 0:
        return 0
    else:
        return num / den
