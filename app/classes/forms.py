# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.validators import URL, Email, DataRequired
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField, URLField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField('Role',choices=[("Teacher","Teacher"),("Student","Student")])
    age = IntegerField('Age', validators=[NumberRange(min=1,max=99)])



class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Post Blog')

class AdviceForm(FlaskForm):
    topic = StringField('Subject', validators=[DataRequired()])
    question = TextAreaField('What is your question?', validators=[DataRequired()])
    priority = IntegerField('How important is this?', validators=[NumberRange(min=1,max=10)])
    submit = SubmitField('Post Advice')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class HikeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    name = SelectField('Hike Name',choices=[("Yosemite's Vernal Falls","Yosemite's Vernal Falls"),("Nevada Falls and Half Dome","Nevada Falls and Half Dome"), ("Redwood National Park's Tall Trees Grove Loop", "Redwood National Park's Tall Trees Grove Loop"), ("Channel Islands National Park's Prisoners Harbor Trail", "Channel Islands National Park's Prisoners Harbor Trail"), ("Other", "Other")])
    text = TextAreaField('Write your Review', validators=[DataRequired()])
    subject = SelectField('Experiences',choices=[("Point To Point", "Point To Point"), ("Loop","Loop"), ("Trail", "Trail"), ("Other","Other")])
    rating = IntegerField('Rate your experience: 0 is terrible, 10 is amazing', validators=[NumberRange(min=0,max=10, message="Enter a number between 0 and 10.")])
    submit = SubmitField('Post Review')

class ReplyForm(FlaskForm):
    text = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Post')