""" Specifies routing for the application"""
from re import I
from turtle import title
from flask import render_template, request, jsonify, session
from app import app
from app import database as db_helper

# global variables to keep track of user
# userloged = False


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


@app.route("/logincheck", methods=['POST'])
def logincheck():
    """ logincheck """
    data = request.get_json()
    userinfo = db_helper.search_user(data)
    if userinfo == {}:
        return jsonify({'success': False, 'response': 'Incorrect username or password'})
    else:
        return jsonify({'success': True, 'response': 'User info was found.'})


# Page routes
@app.route("/watchlist_page")
def watchlist_page():
    """ display watchlist """
    data = session.get('user')
    items = db_helper.fetch_watch_by_userid(data)
    return render_template("watchlist.html", watchlist=items)


@app.route("/search_page")
def search_page():
    """ display search result """
    return render_template("search.html")


@app.route("/userpage")
def userpage():
    """ display user page """
    userinfo = session.get('user')
    # print(userinfo['name'])
    return render_template("userpage.html", user=userinfo)


@app.route("/search_result")
def search_result():
    """ display search result """
    searched_list = session.get('movie_list', None)
    return render_template("search_result.html", items=searched_list)


@app.route("/movieintro")
def movieintro():
    """ display movie intro page """
    user = session.get('user', None)
    data = session.get('movie_info', None)
    comments = session.get('comment', None)
    return render_template("movieintro.html", uid=user['userID'], id=data['movie_id'], title=data['title'], overview=data['overview'], poster_path=data['poster_path'], comment=comments)


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
    flag = session.get('userlogged')
    if (flag):
        data = session.get('user')
        recommend = db_helper.fetch_recommendations(data["userID"])
        rankitems = db_helper.fetch_movie_ranking()
        return render_template("homepage.html", ranking=rankitems, recommend=recommend)
    else:
        return render_template("login.html")


@app.route("/homeranking")
def homepage_ranking():
    """ returns rendered homepage """
    items = db_helper.fetch_movie_ranking()
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


@app.route("/registerinfo", methods=['POST'])
def register():
    try:
        data = request.get_json()
        ret = db_helper.insert_user(data)
        if ret == {}:
            session.clear()
            session['userlogged'] = False
        else:
            session.clear()
            session['userlogged'] = True
            user = db_helper.search_user_by_id(data)
            session['user'] = user
            result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)


@app.route("/verify_user", methods=['POST'])
def verify_user():
    try:
        data = request.get_json()
        user = db_helper.search_user(data)
        if user == {}:
            print("User not found")
            session.clear()
            session['userlogged'] = False
            result = {'success': False, 'response': 'User not found'}
        else:
            print("User found")
            print(data['userID'])
            print(session.get('userlogged'))
            items = db_helper.search_user_by_id(data)
            print("asasa")
            session.clear()
            session['user'] = items
            session['userlogged'] = True
            result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)

# filter movie by genre
# input genrename-value pair 1 for chosen


@app.route("/genre_filter", methods=['POST'])
def genre_filter():
    """ returns rendered rootpage """
    data = request.get_json()
    items = db_helper.genre_filter(data)
    session.clear()
    session['movie_list'] = items
    searched_list = session.get('movie_list', None)
    return render_template("search_result.html", items=searched_list)

# add new comment
# input is userID, movie_id, rating, msg,


@app.route("/create_comment", methods=['POST'])
def create_comment():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_comment(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

# for single movie page (with get_movie_info)
# input is the movie id


@app.route("/movie_comment", methods=['POST'])
def get_comment_by_movie():
    data = request.get_json()
    items = db_helper.fetch_comment_by_movieid(data)
    return render_template("movie_comment.html", items=items)

# add to watchlist
# input is userID, movie_id


@app.route("/create_watchlist_item", methods=['POST'])
def create_watchlist_item():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_watch(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

# for user home page
# input is the user id


@app.route("/user_watchlist", methods=['POST'])
def get_watchlist():
    data = request.get_json()
    session['watchlist'] = db_helper.fetch_watch_by_userid(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

# get userinfo by id
# input is the user id


@app.route("/userpage")
def get_userinfo_by_user():
    items = session.get('user')
    return render_template("userpage.html", items=items)

# for single movie page (with get_comment_by_movie)
# input is the movie id


@app.route("/movie_info", methods=['POST'])
def get_movie_info():
    data = request.get_json()
    session['movie_info'] = db_helper.search_movie_by_id(data)
    session['comment'] = db_helper.fetch_comment_by_movieid(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/get_recommend", methods=['POST'])
def get_recommend():
    data = request.get_json()
    print("vevrv")
    session['recommend'] = db_helper.fetch_recommendations(data["userID"])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)
