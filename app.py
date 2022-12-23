from flask import *
from flask_login import *

import os
from scripts.db import DB
from werkzeug.security import *
from UserLogin import UserLogin

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)


# --- Root ---

@app.route('/')
def root_index():
    return render_template('views/index.html')

# --- Users ---

@app.route('/users')
def users_index():
    users_data = DB().get_all_from_table('auth')
    return render_template('views/users/index.html', users=users_data)

@app.route('/users/<id>', methods=['POST', 'GET'])
def users_show(id=None):
    if request.method == 'POST':
        if request.form['action'] == 'delete':
            DB().delete_user_by_id(id)
            return redirect(url_for('users_index'))
    elif request.method == 'GET':
        user_data = DB().get_user_by_id(id)
        return render_template('views/users/profile.html', user=user_data)

@app.route("/login" , methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = DB().getUserByEmail(request.form['email'])
        if user and check_password_hash(user[0][3] , request.form['psw']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)
            return redirect(url_for('users_show', id=user[0][0]))
        flash("Неверная пара логин/пароль" , "error")
    return render_template("views/login.html")

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request. form['psw2']:
            hash = generate_password_hash((request.form['psw']))
            res = DB().AddUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                redirect(url_for('login'))
            else:
                flash("ошибка при добавлении в дб", "error")

        else:
            flash("Неверно заполнены поля", "error")
    return render_template("views/register.html")



