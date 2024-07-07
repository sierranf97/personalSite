from datetime import datetime, date
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
import smtplib
from forms import CreatePostForm, ContactForm
from dotenv import load_dotenv, dotenv_values
import sqlite3

load_dotenv()
my_secrets = dotenv_values(".env")

app = Flask(__name__)
app.config['SECRET_KEY'] = my_secrets['WEBSITE_KEY']
ckeditor = CKEditor(app)
Bootstrap5(app)

my_email = "sierranf97@gmail.com"
password = my_secrets['EMAIL_PASSWORD']


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///newsfeed.db"
# initialize the app with the extension
db.init_app(app)


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_type: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)
    img_alt: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.context_processor
def inject_now():
    return {'now': datetime.today().strftime('%Y')}


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/newsfeed')
def news():
    return render_template("newsfeed.html")


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(Post, post_id)
    return render_template("post.html", post=requested_post)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == 'GET':
        return render_template("contact.html", form=form)
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        contents = f"{name}\n\n{email}\n\n{message}"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:New message from your website!\n\n{contents}"
            )
        return redirect(url_for('sent'))
    else:
        new_form = ContactForm(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        if request.form['name'] == "":
            flash("Name is required")
        if request.form['message'] == "":
            flash("A message is required")
        return render_template("contact.html", form=new_form)


@app.route('/website-info')
def info():
    return render_template("websiteinfo.html")


@app.route('/message-sent')
def sent():
    return render_template("messagesent.html")


@app.route('/create', methods=["GET", "POST"])
def create():
    input_password = request.args.get('pass')
    form = CreatePostForm()
    if input_password == my_secrets['ADMIN_PASSWORD'] and request.method == 'GET':
        return render_template('create.html', form=form)

    if form.validate_on_submit():
        new_post = Post(
            post_type=request.form['type'],
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            date=date.today().strftime("%B %d, %Y"),
            body=request.form['body'],
            img_url=request.form['img_url'],
            img_alt=request.form['img_alt'],
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("news"))
    elif request.method == 'POST':
        flash(str(form.errors.items()))
        print(form.errors.items())
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
