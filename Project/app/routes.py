""" Specifies routing for the application"""
from flask import render_template, request, jsonify, session
from app import app
from app import database as db_helper


@app.route("/delete/<int:movie_id>", methods=['POST'])
def delete(movie_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_movie_by_id(movie_id)
        result = {'success': True, 'response': 'Removed movie'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:movie_id>", methods=['POST'])
def update(movie_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        db_helper.update_movie_entry(movie_id, data)
        result = {'success': True, 'response': 'Movie Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_movie(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/search_movie", methods=['POST'])
def search_movie():
    """ search movie"""
    data = request.get_json()
    searched_list = db_helper.search_movie_by_title(data)
    session.clear()
    session['movie_list'] = searched_list
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/adv_query_0", methods=['POST'])
def advanced_0():
    """ advanced_query_0 """
    query_list = db_helper.advanced_query_0()        # advanced one
    session.clear()
    session['adv_query_0'] = query_list
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/adv_query_1", methods=['POST'])
def advanced_1():
    """ advanced_query_1 """
    query_list = db_helper.advanced_query_1()
    session.clear()
    session['adv_query_1'] = query_list
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

# Page routes
@app.route("/search_page")
def search_page():
    """ display search result """
    return render_template("search.html")


@app.route("/search_result")
def search_result():
    """ display search result """
    searched_list = session.get('movie_list', None)
    return render_template("search_result.html", items=searched_list)


@app.route("/adv_result_0")
def advanced_result_0():
    """ returns rendered homepage """
    query_list = session.get('adv_query_0', None)
    return render_template("adv_result_0.html", items=query_list)


@app.route("/adv_result_1")
def advanced_result_1():
    """ returns rendered homepage """
    query_list = session.get('adv_query_1', None)
    return render_template("adv_result_1.html", items=query_list)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_movie()
    return render_template("homepage.html", items=items)


@app.route("/advancedop")
def rootpage():
    """ returns rendered rootpage """
    items = db_helper.fetch_movie()
    return render_template("root.html", items=items)


@app.route("/login")
def loginpage():
    """ returns rendered login page """
    return render_template("login.html")


@app.route("/register")
def registerpage():
    " returns rendered register page """
    return render_template("register.html")


@app.route("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        db_helper.insert_user(data)
        result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)


@app.route("/check_user", methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        user = db_helper.search_user(data)
        session.clear()
        session['adv_query_1'] = user
        result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)
