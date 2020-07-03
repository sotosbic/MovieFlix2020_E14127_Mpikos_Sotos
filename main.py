from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from pprint import pprint
from mongo import Mongo

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(mail, password):
    user_check = Mongo().auth_check(mail, password)
    Mongo().close()
    return user_check

@auth.get_user_roles
def get_user_roles(user):
    user_role = Mongo().getCategoty(user['username'])
    Mongo().close()
    return user_role

@app.route('/user/search')
@auth.login_required()
def user_search():
    
    args = {
        "title" : request.args.get('title'),
        "year" : request.args.get('year'),
        "actors" : request.args.get('actors')
    }

    args = { k:v for k,v in args.items() if v is not None }

    res = Mongo().db.Movies.find(args)
    Mongo().close()
    return res

@app.route('/user/show_info')
@auth.login_required()
def user_show_info():

    args = {
        "title": request.args.get('title')
    }
    res = Mongo().db.Movies.find(args)
    Mongo().close()
    return res 


@app.route('/user/show_comments')
@auth.login_required()
def user_show_comments():
    args = {
        "title": request.args.get('title')
    }
    res = Mongo().db.Movies.find(args)[0]['comments']
    Mongo().close()
    return res

@app.route('/user/rating')
@auth.login_required()
def user_rating():
    args = {
        "title": request.args.get('title')
    }
    res = Mongo().db.Movies.find(args)[0]['rating']
    Mongo().close()
    return res

@app.route('/user/remove_rating')
@auth.login_required()
def user_remove_rating():
    return "Hello, {}!".format(auth.current_user())


@app.route('/user/add_comment')
@auth.login_required()
def user_add_comment():
    title = request.args.get('title')
    comment = request.args.get('comment')
    res = Mongo().db.Movies.update({"title": title},{ '$push' : {auth.current_user(): comment}})
    
    Mongo().close()
    return "Comment added"


@app.route('/user/show_user_comments')
@auth.login_required()
def user_show_user_comments():
    return "Hello, {}!".format(auth.current_user())


@app.route('/user/user_ratings')
@auth.login_required()
def user_ratings():
    return "Hello, {}!".format(auth.current_user())


@app.route('/user/delete_comment')
@auth.login_required()
def user_delete_comment():
    return "Hello, {}!".format(auth.current_user())


@app.route('/user/delete_account')
@auth.login_required()
def user_delete_account():
    return Mongo().db.Users.remove({"e-mail": auth.current_user()})


@app.route('/admin/add_movie')
@auth.login_required(role="admin")
def admin_add_movie():
    return "Hello, {}!".format(auth.current_user())


@app.route('/admin/delete_movie')
@auth.login_required(role="admin")
def admin_delete_movie():
    return "Hello, {}!".format(auth.current_user())


@app.route('/admin/update_movie')
@auth.login_required(role="admin")
def admin_update_movie():
    return "Hello, {}!".format(auth.current_user())

@app.route('/admin/delete_comment')
@auth.login_required(role="admin")
def admin_delete_comment():
    return "Hello, {}!".format(auth.current_user())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
