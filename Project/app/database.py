"""Defines all the functions related to the database"""
# from asyncio.windows_events import NULL
from app import db
from datetime import datetime


def fetch_movie() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting database")
    query_results = conn.execute(
        "Select * from movie_info LIMIT 10;").fetchall()
    conn.close()
    movie_list = []
    for result in query_results:
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": result[7],
            "popularity": result[8],
            "revenue": result[9],
        }
        movie_list.append(item)

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
    query = 'Select * From movie_info where title like "%%{}%%" LIMIT 10;'.format(
        data['title'])
    # if (data['movie_id'] != NULL):
    #     query = 'Select * From movie_info where movie_id = {} LIMIT 40;'.format(data['movie_id'])
    print(query)
    query_results = conn.execute(query).fetchall()
    conn.close()
    movie_list = []
    for result in query_results:
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": result[7],
            "popularity": result[8],
            "revenue": result[9],
        }
        movie_list.append(item)

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


def insert_user(data: dict) -> None:
    conn = db.connect()
    query_results = conn.execute(
        "Select max(userID) from account_info;").fetchall()
    # query_results = [x for x in query_results]
    movie_id = query_results[0][0] + 1
    data['userID'] = movie_id
    query = 'Insert Into account_info (userID, account_name, account_passwd, age) VALUES ("{}", "{}", "{}","{}");'.format(
        data['userID'], data["name"], data["password"], data["age"])
    conn.execute(query)
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


def genre_fliter(data: dict) -> list:
    conn = db.connect()
    print("Starting genre_fliter")

    genre_list = []
    for genre in data:
        if data[genre] == 1:
            genre_list.append(genre)

    query_results = conn.execute(
        "Select genre_id from genre where genre_name in '{}';".format(tuple(genre_list))).fetchall()
    genre_id_list = [result[0] for result in query_results]
    query_results = conn.execute("Select distinct movie_id from movie_genre where genre_id in '{}';".format(
        tuple(genre_id_list))).fetchall()
    movie_id_list = [result[0] for result in query_results]
    query_results = conn.execute(
        "Select * from movie_info where movie_id in '{}' limit 20;".format(tuple(movie_id_list))).fetchall()
    conn.close()
    movie_list = []
    for result in query_results:
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": result[7],
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
        "select a.account_name, c.rating, c.adding_date, c.msg from (Select * from comments where movie_id = '{}') as c natural join account_info as a limit 20;".format(data['movie_id'])).fetchall()
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
    data['watch_add_date'] = datetime.now()
    value_tuple = tuple([value for value in data.values()])
    query = 'Insert Into movie_info (userID, movie_id, watch_id, watch_add_date) VALUES {};'.format(
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
    movie_id_list = [result[0] for result in query_results]
    query_results = conn.execute(
        "Select * from movie_info where movie_id in '{}' limit 20;".format(tuple(movie_id_list))).fetchall()
    conn.close()
    movie_list = []
    for result in query_results:
        item = {
            "movie_id": result[0],
            "title": result[1],
            "imdb_id": result[2],
            "release_date": result[3],
            "overview": result[4],
            "tagline": result[5],
            "homepage": result[6],
            "poster_path": result[7],
            "popularity": result[8],
            "revenue": result[9],
        }
        movie_list.append(item)
    return movie_list
