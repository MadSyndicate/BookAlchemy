from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date, default=None)
    date_of_death = db.Column(db.Date, default=None)

    def __repr__(self):
        return (f"<Author"
                f" name={self.name!r}"
                f" birth_date={self.birth_date!r}"
                f" date_of_death={self.date_of_death!r}>")

    def __str__(self):
        return (f"Author: {self.name!r},"
                f" Birth_Date: {self.birth_date!r},"
                f"Date_of_Death: {self.date_of_death!r}")

class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    author = db.relationship("Author", backref="books")
    isbn = db.Column(db.String) # for leading zeros
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)

    def __repr__(self):
        return (f"<Book"
                f" title={self.title!r}"
                f" isbn={self.isbn!r}"
                f" publication_year={self.publication_year!r}>")

    def __str__(self):
        return (f"Book: {self.name!r},"
                f" ISBN: {self.isbn!r},"
                f" Publication Year: {self.publication_year!r}")
