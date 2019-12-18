import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request, session, flash
from passlib.hash import sha512_crypt
from sqlalchemy.orm import sessionmaker

from register import *

engine = create_engine('sqlite:///stronger.db', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db = Session()

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def home():
    loggedin_user = session.get("username")
    return render_template("index.html", username=loggedin_user)

@app.route('/user_profile')
def user_profile():
    loggedin_user = session.get("username")

    Session = sessionmaker(bind=engine)
    s = Session()
    email_query = s.query(User_reg.email).filter(User_reg.username.in_([loggedin_user]))
    email_result = email_query.first()
    email_out = [item for letter in email_result for item in letter]
    email_out = ''.join(email_out)

    name_query = s.query(User_reg.name).filter(User_reg.username.in_([loggedin_user]))
    name_result = name_query.first()
    name_out = [item for letter in name_result for item in letter]
    name_out = ''.join(name_out)

    # SFWA
    sfwa_vals_names = s.query(SFWA.name).filter(Bookmark.sfwa_id == SFWA.id)
    sfwa_vals_n_final = sfwa_vals_names.all()
    sfwa_vals_n_list = [item for letter in sfwa_vals_n_final for item in letter]

    sfwa_vals_images = s.query(SFWA.image).filter(Bookmark.sfwa_id == SFWA.id)
    sfwa_vals_i_final = sfwa_vals_images.all()
    sfwa_vals_i_list = [item for letter in sfwa_vals_i_final for item in letter]

    sfwa_vals_links = s.query(SFWA.name).filter(Bookmark.sfwa_id == SFWA.id)
    sfwa_vals_l_final = sfwa_vals_links.all()
    sfwa_vals_l_list = [item for letter in sfwa_vals_l_final for item in letter]

    # YABOOK
    yabook_vals_names = s.query(YABOOK.name).filter(Bookmark.yabook_id == YABOOK.id)
    yabook_vals_n_final = yabook_vals_names.all()
    yabook_vals_n_list = [item for letter in yabook_vals_n_final for item in letter]

    yabook_vals_images = s.query(YABOOK.image).filter(Bookmark.yabook_id == YABOOK.id)
    yabook_vals_i_final = yabook_vals_images.all()
    yabook_vals_i_list = [item for letter in yabook_vals_i_final for item in letter]

    yabook_vals_links = s.query(YABOOK.name).filter(Bookmark.yabook_id == YABOOK.id)
    yabook_vals_l_final = yabook_vals_links.all()
    yabook_vals_l_list = [item for letter in yabook_vals_l_final for item in letter]

    # BOOKCHOR
    bookchor_vals_names = s.query(BOOKCHOR.name).filter(Bookmark.bookchor_id == BOOKCHOR.id)
    bookchor_vals_n_final = bookchor_vals_names.all()
    bookchor_vals_n_list = [item for letter in bookchor_vals_n_final for item in letter]

    bookchor_vals_images = s.query(BOOKCHOR.image).filter(Bookmark.bookchor_id == BOOKCHOR.id)
    bookchor_vals_i_final = bookchor_vals_images.all()
    bookchor_vals_i_list = [item for letter in bookchor_vals_i_final for item in letter]

    bookchor_vals_links = s.query(BOOKCHOR.name).filter(Bookmark.bookchor_id == BOOKCHOR.id)
    bookchor_vals_l_final = bookchor_vals_links.all()
    bookchor_vals_l_list = [item for letter in bookchor_vals_l_final for item in letter]

    return render_template("user_profile.html", username=loggedin_user.capitalize(), name=name_out.capitalize(), email=email_out.capitalize()
                           , sfwa_names=sfwa_vals_n_list, sfwa_images=sfwa_vals_i_list, sfwa_links=sfwa_vals_l_list, sfwa_len=len(sfwa_vals_n_list)
                           , yabook_names=yabook_vals_n_list, yabook_images=yabook_vals_i_list, yabook_links=yabook_vals_l_list, yabook_len=len(yabook_vals_n_list)
                           , bookchor_names=bookchor_vals_n_list, bookchor_images=bookchor_vals_i_list, bookchor_links=bookchor_vals_l_list, bookchor_len=len(bookchor_vals_n_list)
                           )

@app.route('/books')
def books():
    if not session.get('logged_in'):
        return render_template("books.html")
    loggedin_user = session.get("username")
    return render_template("books.html", username=loggedin_user.capitalize())

@app.route('/sfwa_books')
def sfwa_books():
    loggedin_user = session.get("username")

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

    Session = sessionmaker(bind=engine)
    s = Session()
    for i in range(0, len(book_titles)):
        book_name = book_titles[i]
        book_image = images[i]
        book_link = links_to_web[i]
        query = s.query(SFWA).filter(SFWA.name.in_([book_name]))
        result = query.first()
        if result is None:
            new_bookmark = SFWA(name=book_name, image=book_image, link=book_link)
            db.add(new_bookmark)
            db.commit()

    id_query = s.query(SFWA.id)
    id_result = id_query.all()
    out = [item for id in id_result for item in id]

    return render_template("sfwa_books.html", id_result=out, username=loggedin_user, book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/yabook_books')
def yabook_books():
    loggedin_user = session.get("username")

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

    Session = sessionmaker(bind=engine)
    s = Session()
    for i in range(0, len(book_titles)):
        book_name = book_titles[i]
        book_image = images[i]
        book_link = links_to_web[i]
        query = s.query(YABOOK).filter(YABOOK.name.in_([book_name]))
        result = query.first()
        if result is None:
            new_bookmark = YABOOK(name=book_name, image=book_image, link=book_link)
            db.add(new_bookmark)
            db.commit()

    id_query = s.query(YABOOK.id)
    id_result = id_query.all()
    out = [item for id in id_result for item in id]

    return render_template("yabook_books.html", id_result=out, username=loggedin_user, book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/bookchor_books')
def bookchor_books():
    loggedin_user = session.get("username")

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

    Session = sessionmaker(bind=engine)
    s = Session()
    for i in range(0, len(book_titles)):
        book_name = book_titles[i]
        book_image = images[i]
        book_link = links_to_web[i]
        query = s.query(BOOKCHOR).filter(BOOKCHOR.name.in_([book_name]))
        result = query.first()
        if result is None:
            new_bookmark = BOOKCHOR(name=book_name, image=book_image, link=book_link)
            db.add(new_bookmark)
            db.commit()

    id_query = s.query(BOOKCHOR.id)
    id_result = id_query.all()
    out = [item for id in id_result for item in id]

    return render_template("bookchor_books.html", id_result=out, username=loggedin_user, book_titles=book_titles, images=images, len=len(images), links_to_web=links_to_web)

@app.route('/sfwa_bookmark', methods=['GET', 'POST'])
def sfwa_bookmark():
    loggedin_user = session.get("username")

    if request.method == 'POST':
        index = request.form['index']

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Bookmark).filter(Bookmark.user_id.in_([loggedin_user]), Bookmark.sfwa_id.in_([index]))
        result = query.first()
        if result is None:
            bookmark_no = Bookmark(user_id=loggedin_user, sfwa_id=index)
            db.add(bookmark_no)
            db.commit()
            return redirect(url_for('sfwa_books'))
        else:
            flash("Already bookmarked")
            return redirect(url_for('sfwa_books'))
    return redirect(url_for('home'))

@app.route('/yabook_bookmark', methods=['GET', 'POST'])
def yabook_bookmark():
    loggedin_user = session.get("username")

    if request.method == 'POST':
        index = request.form['index']

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Bookmark).filter(Bookmark.user_id.in_([loggedin_user]), Bookmark.yabook_id.in_([index]))
        result = query.first()
        if result is None:
            bookmark_no = Bookmark(user_id=loggedin_user, yabook_id=index)
            db.add(bookmark_no)
            db.commit()
            return redirect(url_for('yabook_books'))
        else:
            flash("Already bookmarked")
            return redirect(url_for('yabook_books'))
    return redirect(url_for('home'))

@app.route('/bookchor_bookmark', methods=['GET', 'POST'])
def bookchor_bookmark():
    loggedin_user = session.get("username")

    if request.method == 'POST':
        index = request.form['index']

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Bookmark).filter(Bookmark.user_id.in_([loggedin_user]), Bookmark.bookchor_id.in_([index]))
        result = query.first()
        if result is None:
            bookmark_no = Bookmark(user_id=loggedin_user, bookchor_id=index)
            db.add(bookmark_no)
            db.commit()
            return redirect(url_for('bookchor_books'))
        else:
            flash("Already bookmarked")
            return redirect(url_for('bookchor_books'))
    return redirect(url_for('home'))

@app.route('/login')
def go_login():
    return render_template("login.html")

@app.route('/login')
def login(post=1):
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return home()

@app.route('/login', methods=['POST'])
def do_login():
    session['username'] = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    secure_password = sha512_crypt.encrypt(POST_PASSWORD)

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User_reg).filter(User_reg.username.in_([session['username']]), User_reg.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return login(session['username'])

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

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User_reg).filter(User_reg.username.in_([session.get('username')]))
        result = query.first()
        # usernamedata = db.execute("SELECT username FROM all_users WHERE username=:username", {"username":username}).fetchone()
        if result is None:
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
