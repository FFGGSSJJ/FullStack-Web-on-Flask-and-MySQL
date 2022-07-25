"""Defines all the functions related to the database"""
from app import db


def fetch_movie() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    print("Starting database")
    query_results = conn.execute("Select * from movie_info;").fetchall()
    conn.close()
    todo_list = []
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
        todo_list.append(item)

    return todo_list


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
        query += '{} = {}, '.format(attr, value)
    if query[-2:] == ', ':
        query = query[:-2]+' where movie_id = {};'.format(movie_id)
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
    query = 'Insert Into movie_info (movie_id, title, release_date, overview, tagline) VALUES {};'.format(value_tuple)
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
