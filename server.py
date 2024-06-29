from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
import smtplib
from forms import CreatePostForm, ContactForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ds37fw4&C#ce120cenw'
# os.environ.get('BLOG_SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

my_email = "sierranf97@gmail.com"
password = "udxgrtacidodifbd"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
db.init_app(app)


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


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == 'GET':
        return render_template("contact.html", form=form)
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        contents = (f"{name}\n\n{email}\n\n{message}")

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
        if request.form['name'] is "":
            flash("Name is required")
        if request.form['message'] is "":
            flash("A message is required")
        return render_template("contact.html", form=new_form)


@app.route('/website-info')
def info():
    return render_template("websiteinfo.html")


@app.route('/message-sent')
def sent():
    return render_template("messagesent.html")


if __name__ == "__main__":
    app.run(debug=True)