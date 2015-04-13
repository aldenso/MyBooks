from flask import render_template, flash, redirect, session, url_for, request, g, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, AddBook, UpdateBook, AddAuthor, UpdateAuthor, AddPublisher, UpdatePublisher
from .models import User, Author, Book, Publisher
import json, datetime
from config import POSTS_PER_PAGE

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/about')
def aboutpage():
    title = "About this page."
    paragraph = ["To obtain more info about this page please contact:"]

    pageType = 'contact'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)

@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Welcome to My Inventory of Books"
    user = g.user
    posts = ["This site is used to serve as an inventory of books, authors and publishers",
            "The idea is to create first the Authors and Publishers, then create the Books"]
    return render_template('index.html',
                       title=title,
                       user=user,
                       posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    title = "Add new book"
    error = None
    form = AddBook()
    if form.validate_on_submit():
    #if request.method == 'POST':
        authorfullname = request.form['author']
        publishername = request.form['publisher']
        author = Author.query.filter_by(fullname=authorfullname).first()
        publisher = Publisher.query.filter_by(name=publishername).first()
        timestamp=datetime.datetime.utcnow()
        book = Book(title=form.title.data, year=form.year.data, 
        author_id=author.id, publisher_id=publisher.id,
        synopsis=form.synopsis.data, timestamp=timestamp)
        db.session.add(book)
        db.session.commit()
        flash("New Book added successfully")
        return redirect(url_for('add_book'))
    return render_template('add_book.html',
                           title=title, error=error, form=form)

@app.route('/update_book', methods=['GET','POST'])
@login_required
def update_book():
    title = "Update Book Information"
    user = g.user
    bookid = request.args.get('bookid')
    book = Book.query.get(bookid)
    author = Author.query.get(book.author_id)
    publisher = Publisher.query.get(book.publisher_id)
    form = UpdateBook(id=bookid)
    if request.method == 'POST':
        bookid = form.id.data
        book = Book.query.get(bookid)
        author = Author.query.get(book.author_id)
        publisher = Publisher.query.get(book.publisher_id)
        form = UpdateBook(id=bookid)
        if form.title.data and form.year.data and form.synopsis.data:
            book.title = form.title.data
            book.year = form.year.data
            book.synopsis = form.synopsis.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
            author=author, publisher=publisher))
        elif form.title.data and form.year.data:
            book.title = form.title.data
            book.year = form.year.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif form.year.data and form.synopsis.data:
            book.year = form.year.data
            book.synopsis = form.synopsis.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif form.title.data and form.synopsis.data:
            book.title = form.title.data
            book.synopsis = form.synopsis.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif form.title.data:
            book.title = form.title.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif form.year.data:
            book.year = form.year.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif form.synopsis.data:
            book.synopsis = form.synopsis.data
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif request.form['author'] and request.form['publisher']:
            author = Author.query.filter_by(fullname=request.form['author']).first()
            publisher = Publisher.query.filter_by(name=request.form['publisher']).first()
            book.author_id = author.id
            book.publisher_id = publisher.id
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif request.form['author']:
            author = Author.query.filter_by(fullname=request.form['author']).first()
            book.author_id = author.id
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        elif request.form['publisher']:
            publisher = Publisher.query.filter_by(name=request.form['publisher']).first()
            book.publisher_id = publisher.id
            db.session.commit()
            flash("Book Updated")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
        else:
            flash("You must introduce new values to change")
            return redirect(url_for('update_book', bookid=bookid,
              author=author, publisher=publisher))
    return render_template('update_book.html', 
      title=title, user=user, book=book, form=form, author=author,
       publisher=publisher)

@app.route('/delete_book', methods=['POST'])
def delete_book():
    book = request.form['bookid']
    removebook = Book.query.get(book)
    db.session.delete(removebook)
    db.session.commit()
    flash("Book successfully removed.")
    return redirect(url_for('show_books'))

@app.route('/info_book')
def info_book():
    title = "Book Information"
    bookid = request.args.get('bookid')
    book = Book.query.join(Author, Publisher).add_columns(Book.title, 
        Author.fullname, Publisher.name, Book.year, Book.synopsis, 
        Book.timestamp, Book.id).filter(Book.id==bookid).first()
    return render_template('info_book.html', book=book, title=title)


@app.route('/show_books')
@app.route('/show_books/<int:page>')
@login_required
def show_books(page=1):
    title = "Inventory of Books"
    user = g.user
    numbooks = Book.query.count()
    books = Book.query.join(Author, Publisher).add_columns(Book.title,
        Author.fullname, Publisher.name, Book.year, Book.id).paginate(page,
        POSTS_PER_PAGE, False)
    return render_template('show_books.html',
                           title=title, user=user, books=books,
                           numbooks=numbooks)


@app.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    title = "Add new author"
    user = g.user
    form = AddAuthor()
    if form.validate_on_submit():
    #if request.method == 'POST':
        newauthor = Author(firstname=form.firstname.data,
                  lastname=form.lastname.data,
                  fullname=form.firstname.data +' '+ form.lastname.data,
                  biography=form.biography.data)
        db.session.add(newauthor)
        db.session.commit()
        flash("New Author added.")
        return redirect(url_for('add_author'))
    return render_template('add_author.html',
                           title=title, user=user, form=form)

@app.route('/delete_author', methods=['POST'])
def delete_author():
    author = request.form['authorid']
    removeauthor = Author.query.get(author)
    db.session.delete(removeauthor)
    db.session.commit()
    flash("Author successfully removed.")
    return redirect(url_for('list_authors'))


@app.route('/list_authors')
@app.route('/list_authors/<int:page>')
@login_required
def list_authors(page=1):
    title = "List of Authors"
    user = g.user
    numauthors = Author.query.count()
    authors = Author.query.paginate(page, POSTS_PER_PAGE, False)
    return render_template('list_authors.html',
                           title=title, user=user, authors=authors,
                           numauthors=numauthors)


@app.route('/update_author', methods=['GET', 'POST'])
@login_required
def update_author():
    title = "Update Author Information"
    user = g.user
    authorid = request.args.get('authorid')
    author = Author.query.get(authorid)
    form = UpdateAuthor(id=authorid)
    if form.validate_on_submit():
  #if request.method == 'POST':
        authorid = form.id.data
        author = Author.query.get(authorid)
        if form.firstname.data and form.lastname.data and form.biography.data:
            author.firstname=form.firstname.data
            author.lastname=form.lastname.data
            author.fullname=form.firstname.data +' '+form.lastname.data
            author.biography=form.biography.data
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.firstname.data and form.lastname.data:
            author.firstname=form.firstname.data
            author.lastname=form.lastname.data
            author.fullname=form.firstname.data +' '+form.lastname.data
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.firstname.data and form.biography.data:
            author.firstname=form.firstname.data
            author.lastname=form.biography.data
            author.fullname=form.firstname.data +' '+author.lastname
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.lastname.data and form.biography.data:
            author.lastname=form.lastname.data
            author.fullname=author.firstname +' '+form.lastname.data
            author.biography=form.biography.data
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.firstname.data:
            author.firstname=form.firstname.data
            author.fullname = form.firstname.data +' '+Author.lastname 
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.lastname.data:
            author.lastname=form.lastname.data
            author.fullname = Author.firstname+' '+form.lastname.data
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        elif form.biography.data:
            author.biography=form.biography.data
            db.session.commit()
            flash("Info updated successfully for Author ")
            return redirect(url_for('update_author', authorid=authorid))
        else:
            flash("You must set a value to change")
            return redirect(url_for('update_author', authorid=authorid))
    return render_template('update_author.html',
                   title=title, user=user, author=author, form=form)

@app.route('/info_author')
def info_author():
    title = "Author Information"
    authorid = request.args.get('authorid')
    author = Author.query.filter_by(id=authorid).first()
    books = Book.query.filter_by(author_id=authorid).all()
    return render_template('info_author.html', author=author, books=books,
    title=title)

@app.route('/get_author/<author>', methods=['GET'])
def get_list_author(author):
    #author = request.args.get('author')
    entries = Author.query.filter(Author.fullname.contains(author)).all()
    result = []
    for entry in entries:
        d = {
        'author': entry.fullname
        }
        result.append(d)
    data = json.dumps(result)
    return Response(data,  mimetype='application/json')


@app.route('/add_publisher', methods=['GET', 'POST'])
@login_required
def add_publisher():
    title = "Add new publisher"
    user = g.user
    form = AddPublisher()
    if form.validate_on_submit():
    #if request.method == 'POST':
        newpublisher = Publisher(name=form.name.data,
                  description=form.description.data)
        db.session.add(newpublisher)
        db.session.commit()
        flash("New Publisher added.")
        return redirect(url_for('add_publisher'))
    return render_template('add_publisher.html',
                           title=title, user=user, form=form)

@app.route('/delete_publisher', methods=['POST'])
def delete_publisher():
    publisher = request.form['publisherid']
    removepublisher = Publisher.query.get(publisher)
    db.session.delete(removepublisher)
    db.session.commit()
    flash("Publisher successfully removed.")
    return redirect(url_for('list_publishers'))

@app.route('/list_publishers')
@app.route('/list_publishers/<int:page>')
@login_required
def list_publishers(page=1):
    title = "List of Publishers"
    user = g.user
    numpublishers = Publisher.query.count()
    publishers = Publisher.query.paginate(page, POSTS_PER_PAGE, False)
    return render_template('list_publishers.html',
                           title=title, user=user,
                           publishers=publishers, numpublishers=numpublishers)


@app.route('/update_publisher', methods=['GET', 'POST'])
@login_required
def update_publisher():
    title = "Update Publisher Information"
    user = g.user
    publisherid = request.args.get('publisherid')
    publisher = Publisher.query.get(publisherid)
    form = UpdatePublisher(id=publisherid)
    if form.validate_on_submit():
  #if request.method == 'POST':
        publisherid = form.id.data
        publisher = Publisher.query.get(publisherid)
        if form.name.data and form.description.data:
            publisher.name=form.name.data
            publisher.description=form.description.data
            db.session.commit()
            flash("Info updated successfully for Publisher ")
            return redirect(url_for('update_publisher', publisherid=publisherid))
        elif form.name.data:
            publisher.name=form.name.data
            db.session.commit()
            flash("Info updated successfully for Publisher ")
            return redirect(url_for('update_publisher', publisherid=publisherid))
        elif form.description.data:
            publisher.description=form.description.data
            db.session.commit()
            flash("Info updated successfully for Publisher ")
            return redirect(url_for('update_publisher', publisherid=publisherid))
        else:
            flash("You must set a value to change")
            return redirect(url_for('update_publisher', publisherid=publisherid))
    return render_template('update_publisher.html',
                   title=title, user=user, publisher=publisher, form=form)


@app.route('/get_publisher/<publisher>', methods=['GET'])
def get_list_publisher(publisher):
    entries = Publisher.query.filter(Publisher.name.contains(publisher)).all()
    result = []
    for entry in entries:
        d = {
        'publisher': entry.name
        }
        result.append(d)
    data = json.dumps(result)
    return Response(data,  mimetype='application/json')