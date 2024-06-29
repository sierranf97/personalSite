from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    img_alt = StringField("Image Alt Text", validators=[DataRequired()])
    body = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email (Optional)", validators=[])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
