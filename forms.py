from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    type = SelectField("Post Type", choices=['Event', 'Post'], validators=[DataRequired()])
    title = StringField("Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    date = StringField("Date")
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    img_alt = StringField("Image Alt Text", validators=[DataRequired()])
    body = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired('A name is required')])
    email = EmailField("Email or Phone Number (optional, but very helpful if you'd like me to respond)", validators=[])
    message = TextAreaField("Message", validators=[DataRequired('A message is required')])
    submit = SubmitField("Send Message")


class SoundtrackForm(FlaskForm):
    song_title = StringField("Song Title", validators=[DataRequired('A song title is required')])
    artist = StringField("Artist", validators=[DataRequired('An artist is required')])
    submit = SubmitField("Submit")
