import os
from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime
# from flask_cors import CORS
# from flask_limiter import Limiter
from sqlalchemy import or_
from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = "supersecretkey"   #TODO: to .env

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

# TODO: Check if "needed" + imports
# CORS(app)  # This will enable CORS for all routes
# limiter = Limiter(app=app, key_func=get_remote_address)

@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        author_name = request.form.get('name', None)
        author_birth_date = request.form.get('birthdate', None)
        author_date_of_death = request.form.get('date_of_death', None)

        birth_date = datetime.strptime(author_birth_date, '%Y-%m-%d')\
            if author_birth_date else None
        date_of_death = datetime.strptime(author_date_of_death, '%Y-%m-%d')\
            if author_date_of_death else None

        if not author_name:
            flash("Author name is required", "error")
            return redirect(url_for('home'), code=400)

        author = Author(
            name=author_name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(author)
        db.session.commit()

        flash(f"Author '{author_name}' was added successfully to database!",
              "success")

        return redirect(url_for('home'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        book_title = request.form.get('title', None)
        book_author_id = request.form.get('author_id', None)
        book_isbn = request.form.get('isbn', None)
        book_publication_year = request.form.get('publication_year', None)

        book = Book(
            title=book_title,
            author_id=book_author_id,
            isbn=book_isbn,
            publication_year=book_publication_year
        )

        db.session.add(book)
        db.session.commit()

        flash(f"Book '{book_title}' was added successfully to database!",
              "success")

        return redirect(url_for('home'))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    sort = request.args.get("sort", "title")
    query = request.args.get("q", "").strip()

    books_query = Book.query.join(Author)

    if query:
        search = f"%{query}%"
        books_query = books_query.filter(
            or_(
                Book.title.ilike(search),
                Author.name.ilike(search)
            )
        )

    if sort == "author":
        books_query = books_query.order_by(Author.name)
    else:
        books_query = books_query.order_by(Book.title)

    books = books_query.all()

    if query and not books:
        flash(f"For the search input '{query}' was no matching book title or "
              f"author name found!", "info")

    return render_template('home.html', books=books, sort=sort, query=query)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

    # just once
    """
    with app.app_context():
        db.create_all()
    """
