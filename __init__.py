import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from passlib.hash import sha512_crypt
from sqlalchemy.orm import sessionmaker

from register import *
from tabledef import *

engine = create_engine('sqlite:///stronger.db', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db = Session()

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")

@app.route('/login')
def go_login():
    return render_template("login.html")

@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return home()

# @app.route('/login', methods=['GET', 'POST'])
# def do_login():
#     if request.form['password'] == 'password' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#     else:
#         flash('wrong password!')
#     return home()

@app.route('/login', methods=['POST'])
def do_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    secure_password = sha512_crypt.encrypt(POST_PASSWORD)

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User_reg).filter(User_reg.username.in_([POST_USERNAME]), User_reg.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return login()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        secure_password = sha512_crypt.encrypt(str(password))

        usernamedata = db.execute("SELECT username FROM all_users WHERE username=:username", {"username":username}).fetchone()
        if usernamedata is None:
            if password == confirm:
                user = User_reg(name=name, username=username, email=email, password=password, confirm=secure_password)
                db.add(user)
                db.commit()
                flash("You are registered and can now login", "success")
                return redirect(url_for('home'))
            else:
                flash("Password does not match", "danger")
                return render_template('signup.html')
        else:
            flash("User already exists, please login or contact admin", "danger")
            return render_template('login.html')
    return render_template('signup.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         # do stuff when the form is submitted
#
#         # redirect to end the POST handling
#         # the redirect can be to the same route or somewhere else
#         return redirect(url_for('home'))
#
#         # show the form, it wasn't submitted
#     return render_template('signup.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)