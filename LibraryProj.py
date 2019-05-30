import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

projectDir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(projectDir, "bookdb.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#Add engine for postgre
# engine = create_engine(
    # "postgresql+pg8000://WolfusFlow:db@localhost/test",
    # isolation_level="READ UNCOMMITTED"
# )

class Book(db.Model): #table name also book
    title=db.Column(db.String(80), unique = True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def init():
    books=None
    if request.form:
        try:
          print(request.form)
          book = Book(title=request.form.get("title"))
          db.session.add(book)
          db.session.commit()
        except Exception as e:
            print("Failed to add a book")
            print(e)
    books=Book.query.all()
    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        oldTitle=request.form.get("oldTitle")
        newTitle=request.form.get("newTitle")
        book=Book.query.filter_by(title=oldTitle).first()
        book.title=newTitle
        db.session.commit()
    except Exception as e:
        print("Failed to update the book")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    delTitle=request.form.get("delTitle")
    book=Book.query.filter_by(title=delTitle).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)