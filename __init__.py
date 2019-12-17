import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request, session, flash
from passlib.hash import sha512_crypt
from sqlalchemy.orm import sessionmaker

from register import *
from bookmark import *

engine = create_engine('sqlite:///stronger.db', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db = Session()

bookmark_engine = create_engine('sqlite:///bookmark.db', pool_pre_ping=True)
Bookmark_Session = sessionmaker(bind=bookmark_engine)
bookmark_db = Bookmark_Session()

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def home(post=1):
    return render_template("index.html", username=post)

@app.route('/books')
def books():
    return render_template("books.html")

@app.route('/sfwa_books')
def sfwa_books():
    web_url = "https://www.sfwa.org/featured-books/"
    web_request = requests.get(web_url)
    soup = BeautifulSoup(web_request.text, 'html.parser')

    book_titles = []
    for i in soup.findAll("article", class_="has-post-thumbnail"):
        book_titles.append(i.div.h2.a.get('title'))

    images = []
    for i in soup.findAll("article", class_="has-post-thumbnail"):
        images.append(i.img.get('src'))

    links_to_web = []
    for i in soup.findAll("article", class_="has-post-thumbnail"):
        links_to_web.append(i.div.h2.a.get('href'))

    return render_template("sfwa_books.html", book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/yabook_books')
def yabook_books():
    web_url = "https://www.yabookscentral.com/"
    web_request = requests.get(web_url)
    soup = BeautifulSoup(web_request.text, 'html.parser')

    book_titles = []
    for i in soup.findAll("div", class_="jrListingTitle"):
        book_titles.append(i.a.contents[0])

    images = []
    for i in soup.findAll("div", class_="jrListingThumbnail"):
        images.append(i.a.img.get('src'))

    links_to_web = []
    for i in soup.findAll("div", class_="jrListingThumbnail"):
        links_to_web.append("https://www.yabookscentral.com" + i.a.get('href'))

    return render_template("yabook_books.html", book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/bookchor_books')
def bookchor_books():
    web_url = "https://www.bookchor.com/Featured-Books"
    web_request = requests.get(web_url)
    soup = BeautifulSoup(web_request.text, 'html.parser')

    book_titles = []
    for i in soup.findAll("div", class_="product-item"):
        book_titles.append(i.h3.a.contents[0])
    book_titles = book_titles[:11]

    images = []
    for i in soup.findAll("div", class_="pi-img-wrapper"):
        images.append(i.img.get('src'))
    images = images[:11]

    links_to_web = []
    for i in soup.findAll("div", class_="product-item"):
        links_to_web.append(i.h3.a.get('href'))
    links_to_web = links_to_web[:11]

    return render_template("bookchor_books.html", book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/bookmark', methods=['GET', 'POST'])
def bookmark():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_image = request.form.get('book_image')

        book = User_bookmarks(book_name=book_name, book_image=book_image)
        bookmark_db.add(book)
        bookmark_db.commit()
        req = request.form
        print(req)
    return req

@app.route('/login')
def go_login():
    return render_template("login.html")

@app.route('/login')
def login(post=1):
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return home(post)

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
    return login(POST_USERNAME)

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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
