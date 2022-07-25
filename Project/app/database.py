"""Defines all the functions related to the database"""
from app import db


def fetch_movie() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting database")
    query_results = conn.execute(
        "Select * from movie_info LIMIT 400;").fetchall()
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
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute("Select max(movie_id) from movie_info;")
    query_results = [x for x in query_results]
    movie_id = query_results[0][0] + 1
    data['movie_id'] = movie_id
    attr_tuple = tuple([attr for attr in data.keys()])
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
    query = 'Select * From movie_info where title like "%%{}%%" LIMIT 40;'.format(
        data['title'])
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
            "ave_genre_rating": result[1],
        }
        result_list.append(item)

    return result_list
