"""Defines all the functions related to the database"""
# from asyncio.windows_events import NULL
from app import db
from datetime import datetime
import requests
import pandas as pd
from math import *

genre_dict = {16: "Animation", 35: "Comedy", 10751: "Family", 12: "Adventure", 28: "Action", 53: "Thriller", 18: "Drama", 10749: "Romance", 80: "Crime", 9648: "Mystery", 27: "Horror", 99: "Documentary", 10769: "Foreign", 878: "Science Fiction", 14: "Fantasy", 36: "History", 10752: "War", 10402: "Music", 37: "Western", 10770: "TV Movie",
              11176: "Carousel Productions", 11602: "Vision View Entertainment", 29812: "Telescene Film Group Productions", 2883: "Aniplex", 7759: "GoHands", 7760: "BROSTA TV", 7761: "Mardock Scramble Production Committee", 33751: "Sentai Filmworks", 17161: "Odyssey Media", 18012: "Pulser Productions", 18013: "Rogue State", 23822: "The Cartel"}


def fetch_movie() -> list:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting database")
    query_results = conn.execute(
        "Select * from movie_info LIMIT 10;").fetchall()
    movie_list = []
    for result in query_results:
        query = conn.execute(
            "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
        genre_list = [q[0] for q in query]
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
            "genres": genre_list
        }
        movie_list.append(item)
    conn.close()
    return movie_list


def fetch_movie_ranking() -> list:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting database")
    query_results = conn.execute(
        "Select * from movie_info order by popularity desc LIMIT 10;").fetchall()
    movie_list = []
    for result in query_results:
        query = conn.execute(
            "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
        genre_list = [q[0] for q in query]
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
            "genres": genre_list
        }
        movie_list.append(item)
    conn.close()
    return movie_list


def update_movie_entry(movie_id: int, data: dict) -> None:
    """Updates task description based on given `task_id`
    Args:
        task_id (int): Targeted task_id
        text (str): Updated description
    Returns:
        None
    """
    if data == {}:
        return
    conn = db.connect()
    query = 'Update movie_info set '
    for attr, value in data.items():
        if attr == 'overview' or attr == 'tagline' or attr == 'title':
            query += '{} = "{}", '.format(attr, value)
            continue
        query += '{} = {}, '.format(attr, value)
    if query[-2:] == ', ':
        query = query[:-2]+' where movie_id = {};'.format(movie_id)
        print(query)
        conn.execute(query)
        conn.close()
    return


def insert_new_movie(data: dict) -> int:
    """Insert new movie.
    Returns: The movie_id for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute("Select max(movie_id) from movie_info;")
    query_results = [x for x in query_results]
    movie_id = query_results[0][0] + 1
    data['movie_id'] = movie_id
    value_tuple = tuple([value for value in data.values()])
    query = 'Insert Into movie_info (movie_id, title, release_date, overview, tagline) VALUES {};'.format(
        value_tuple)
    conn.execute(query)
    print("Inserting movie by id: {}".format(movie_id))
    conn.close()
    return movie_id


def remove_movie_by_id(movie_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From movie_info where movie_id = {};'.format(movie_id)
    conn.execute(query)
    print("Removing movie by id {}".format(movie_id))
    conn.close()


def search_movie_by_title(data: dict) -> list:
    """ Search entries based on title """
    conn = db.connect()
    query_results = conn.execute('Select * From movie_info where title like "%%{}%%" LIMIT 5;'.format(
        data['title'])).fetchall()
    # if (data['movie_id'] != NULL):
    #     query = 'Select * From movie_info where movie_id = {} LIMIT 40;'.format(data['movie_id'])
    movie_list = []
    for result in query_results:
        query = conn.execute(
            "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
        genre_list = [q[0] for q in query]
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
            "genres": genre_list
        }
        movie_list.append(item)
    conn.close()
    return movie_list


def advanced_query_0() -> list:
    conn = db.connect()
    query = '''
            SELECT
                c.movie_id,
                title,
                avg(c.rating) as average_rating,
                release_date,
                homepage,
                poster_path
            FROM
                comments c
                join movie_info m on c.movie_id = m.movie_id
            WHERE
                release_date > '2010-1-1'
            GROUP BY
                c.movie_id
            ORDER BY
                average_rating DESC
            LIMIT
                15;
            '''

    query_result = conn.execute(query).fetchall()
    conn.close()
    result_list = []
    for result in query_result:
        item = {
            "movie_id": result[0],
            "title": result[1],
            "average_rating": result[2],
            "release_date": result[3],
            "homepage": result[4],
            "poster_path": result[5],
        }
        result_list.append(item)

    return result_list


def advanced_query_1() -> list:
    conn = db.connect()
    query = '''
            -- ave rating for different genre
            SELECT g.genre_name, avg(temp1.average_rating) as ave_genre_rating
            From 
                movie_genre m_g
                join (SELECT c.movie_id, avg(c.rating) as average_rating
                    FROM comments c join movie_info m on c.movie_id = m.movie_id
                    GROUP BY c.movie_id
                    ORDER BY average_rating DESC) as temp1 on temp1.movie_id = m_g.movie_id
                join genre g on g.genre_id = m_g.genre_id
            GROUP BY g.genre_id
            LIMIT 15;
            '''

    query_result = conn.execute(query).fetchall()
    conn.close()
    result_list = []
    for result in query_result:
        item = {
            "genre_name": result[0],
            "ave_genre_rating": round(result[1], 2),
        }
        result_list.append(item)

    return result_list


def get_tag(name):
    return [k for (k, v) in genre_dict.items() if v == name]


def insert_user(data: dict) -> None:
    print("intert\n\n\n\n\n\n\n")
    conn = db.connect()
    query_results = conn.execute(
        "Select max(userID) from account_info;").fetchall()
    # query_results = [x for x in query_results]
    movie_id = query_results[0][0] + 1
    data['userID'] = movie_id
    data['account_type'] = 1
    i = 0
    genre_list = []
    for genre, value in data.items():
        if genre == "name" or genre == "password" or genre == "age" or genre == 'account_type' or genre == 'userID':
            continue
        if value == 1 and i < 3:
            genre_list.append(genre)
            i = i+1
    print(genre_list)
    data['tags'] = [get_tag(genre)[0] for genre in genre_list]
    print(data['tags'])
    if len(genre_list) == 1:
        query = 'Insert Into account_info (userID, account_name, account_passwd, age, account_type, tag1) VALUES ({}, "{}", "{}",{},{},{});'.format(
            data['userID'], data["name"], data["password"], data["age"], data['account_type'], data['tags'][0][0])
    elif len(genre_list) == 2:
        query = 'Insert Into account_info (userID, account_name, account_passwd, age, account_type, tag1, tag2) VALUES ({}, "{}", "{}",{},{},{},{});'.format(
            data['userID'], data["name"], data["password"], data["age"], data['account_type'], data['tags'][0][0], data['tags'][1][0])
    elif len(genre_list) == 3:
        query = 'Insert Into account_info (userID, account_name, account_passwd, age, account_type, tag1, tag2, tag3) VALUES ({}, "{}", "{}",{},{},{},{},{});'.format(
            data['userID'], data["name"], data["password"], data["age"], data['account_type'], data['tags'][0][0], data['tags'][1][0], data['tags'][2][0])
    else:
        return {}
    conn.execute(query)
    print("asdsdsadsdsadsda\n")
    conn.close()
    return data


def search_user(data: dict) -> None:
    conn = db.connect()
    query = "Select Count(*) From account_info Where userID='{}' and account_passwd='{}';".format(
        data["userID"], data["account_passwd"])
    count = conn.execute(query)
    count = count.fetchall()[0][0]
    conn.close()
    if count == 1:
        return data
    else:
        return {}


def genre_filter(data: dict) -> list:
    conn = db.connect()
    print("Starting genre_filter")

    genre_list = []
    for genre in data:
        if data[genre] == 1:
            genre_list.append(genre)
    print("Select genre_id from genre where genre_name in {};".format(
        tuple(genre_list)))
    query_results = conn.execute(
        "Select genre_id from genre where genre_name in {};".format(tuple(genre_list))).fetchall()
    genre_id_list = [result[0] for result in query_results]
    if len(genre_id_list) == 1:
        query_results = conn.execute(
            "Select distinct movie_id from movie_genre where genre_id = {};".format(genre_id_list[0])).fetchall()
    else:
        query_results = conn.execute("Select distinct movie_id from movie_genre where genre_id in {};".format(
            tuple(genre_id_list))).fetchall()
    movie_id_list = [result[0] for result in query_results]

    query_results = conn.execute(
        "Select * from movie_info where movie_id in {} limit 10;".format(tuple(movie_id_list))).fetchall()
    conn.close()
    movie_list = []
    for result in query_results:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
        }
        movie_list.append(item)
    return movie_list


def insert_comment(data: dict) -> int:
    """Insert new comment.
    Returns: The comment ID for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute(
        "Select max(comment_id) from comments;").fetchall()
    comment_id = query_results[0][0] + 1
    data['comment_id'] = comment_id
    data['adding_date'] = datetime.now()
    value_tuple = tuple([value for value in data.values()])
    query = 'Insert Into movie_info (userID, movie_id, rating, msg, comment_id, adding_date) VALUES {};'.format(
        value_tuple)
    conn.execute(query)
    print("Inserting comments by id: {}".format(comment_id))
    conn.close()
    return comment_id


def fetch_comment_by_movieid(data: dict) -> list:
    """    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting comment")
    query_results = conn.execute(
        "select a.account_name, c.rating, c.adding_date, c.msg from (Select * from comments where movie_id = '{}') as c natural join account_info as a limit 10;".format(data['movie_id'])).fetchall()
    conn.close()
    comments_list = []
    for result in query_results:
        item = {
            "account_name": result[0],
            "rating": result[1],
            "adding_date": result[2],
            "message": result[3],
        }
        comments_list.append(item)
    return comments_list


def insert_watch(data: dict) -> int:
    """Insert new comment.
    Returns: The comment ID for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute(
        "Select max(watch_id) from watch_list;").fetchall()
    watch_id = query_results[0][0] + 1
    data['watch_id'] = watch_id
    data['watch_add_date'] = str(datetime.now())
    value_tuple = tuple([value for value in data.values()])
    query = 'Insert Into watch_list (userID, movie_id, watch_id, watch_add_date) VALUES {};'.format(
        value_tuple)
    conn.execute(query)
    print("Inserting watch by id: {}".format(watch_id))
    conn.close()
    return watch_id


def fetch_watch_by_userid(data: dict) -> list:
    """    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting watch")
    query_results = conn.execute(
        "Select distinct movie_id from watch_list where userID = '{}'limit 20;".format(data['userID'])).fetchall()
    if (query_results == []):
        return []
    movie_id_list = [result[0] for result in query_results]
    if len(movie_id_list) == 1:
        query_results = conn.execute(
            "Select * from movie_info where movie_id = {} limit 20;".format(movie_id_list[0])).fetchall()
    elif len(movie_id_list) > 1:
        query_results = conn.execute(
            "Select * from movie_info where movie_id in {} limit 20;".format(tuple(movie_id_list))).fetchall()
    else:
        conn.close()
        return []
    conn.close()
    movie_list = []
    for result in query_results:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
        }
        movie_list.append(item)
    return movie_list


def search_user_by_id(data: dict) -> None:
    conn = db.connect()
    query = "Select * From account_info Where userID={};".format(
        data["userID"])
    print(query)
    result = conn.execute(query).fetchall()[0]
    print(result)
    genre_list = []
    for index in result[5:8]:
        if index != None:
            genre_list.append(genre_dict[index])
        else:
            genre_list.append('')
    user = {
        "userID": result[0],
        "account_name": result[1],
        "account_passwd": result[2],
        "age": result[3],
        "account_type": result[4],
        "tag1": genre_list[0],
        "tag2": genre_list[1],
        "tag3": genre_list[2],
    }
    conn.close()
    return user


def search_movie_by_id(data: dict) -> None:
    conn = db.connect()
    query = "Select * From movie_info Where movie_id='{}';".format(
        data["movie_id"])
    result = conn.execute(query).fetchall()[0]
    query_results = conn.execute(
        "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
    genre_list = [q[0] for q in query_results]
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        result[0])
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/original/" + poster_path
    item = {
        "movie_id": result[0],
        "title": result[1],
        "imdb_id": result[2],
        "release_date": result[3],
        "overview": result[4],
        "tagline": result[5],
        "homepage": result[6],
        "poster_path": full_path,
        "popularity": result[8],
        "revenue": result[9],
        "genres": genre_list
    }
    conn.close()
    return item


def fetch_prerecommendations(userid) -> dict:
    """Read all similar users based on tags
    Returns:
        A list of dictionaries{userID:{title:rating}}
    """

    conn = db.connect()
    query = "call recommend({});".format(userid)
    print("call recommend({})".format(userid))
    query_results = conn.execute(query).fetchall()
    query = "select * from recommend_table limit 10;"
    query_results = conn.execute(query).fetchall()
    print("\n\n\n\n\n")
    print(query_results)
    # ---------changes------
    query_userid = [q[0] for q in query_results]
    if query_results == [] or userid not in query_userid:
        # ----------------------
        query_results = conn.execute(
            "Select * from movie_info order by popularity desc LIMIT 20;").fetchall()
        movie_list = []
        print("\n\n****************\n\n\n")
        print(query_results)
        query_results = query_results[11:]
        for result in query_results:
            query = conn.execute(
                "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
            genre_list = [q[0] for q in query]
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
                result[0])
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/original/" + poster_path
            item = {
                "movie_id": result[0],
                "title": result[1],
                "imdb_id": result[2],
                "release_date": result[3],
                "overview": result[4],
                "tagline": result[5],
                "homepage": result[6],
                "poster_path": full_path,
                "popularity": result[8],
                "revenue": result[9],
                "genres": genre_list
            }
            movie_list.append(item)
            conn.close()
            return movie_list, 1
    conn.close()
    pre_recommendations = {}
    for result in query_results:
        item = [
            result[0],
            result[1],
            result[2],
            result[3]
        ]
        if not item[0] in pre_recommendations.keys():
            pre_recommendations[item[0]] = {item[2]: item[1]}
        else:
            pre_recommendations[item[0]][item[2]] = item[1]
    return pre_recommendations, 0

# top level fuinction


def fetch_recommendations(user_id) -> list:
    """Read all similar users based on ratings
    Returns:
        A list
    """
    recommendations = []
    data, mode = fetch_prerecommendations(user_id)
    if mode == 1:
        return data
    top_user = similar_users(user_id)[0][0]
    items = data[top_user]

    for item in items.keys():
        if item not in data[user_id].keys():
            recommendations.append((item, items[item]))

    recommendations.sort(key=lambda val: val[1], reverse=True)
    conn = db.connect()
    recommendation_list = []
    i = 0
    print(recommendations)
    for single in recommendations:
        if i >= 10:
            break
        query = "Select * From movie_info Where movie_id='{}';".format(
            single[0])
        result = conn.execute(query).fetchall()[0]
        query_results = conn.execute(
            "Select genre_id from movie_genre where movie_id = '{}';".format(result[0])).fetchall()
        genre_list = [q[0] for q in query_results]
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            result[0])
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original/" + poster_path
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": full_path,
            "popularity": result[8],
            "revenue": result[9],
            "genres": genre_list
        }
        recommendation_list.append(item)
        i = i+1
    conn.close()
    return recommendation_list


def Euclidean(user1, user2):
    """Reads the userID in prerecommendations dict
    Returns:
        A value shows the similarity
    """
    print(user1)
    data = fetch_prerecommendations(user1)
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0

    for key in user1_data.keys():
        if key in user2_data.keys():

            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
    return 1 / (1 + sqrt(distance))


def similar_users(userID):
    """Reads the similarity value of userID stored in dict
    Returns:
        A list of tuples
    """
    res = []
    data = fetch_prerecommendations(userID)
    for user2 in data.keys():
        if not user2 == userID:
            similarity = Euclidean(userID, user2)
            res.append((user2, similarity))
    res.sort(key=lambda val: val[1])
    return res[:10]


# ---------------------------------------------recommendation end-----------------------------------------------
