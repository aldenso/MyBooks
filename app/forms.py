from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, HiddenField, TextField
from wtforms.validators import DataRequired, Optional

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class AddBook(Form):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    #author = StringField('Author', validators=[DataRequired()])
    #publisher = StringField('Publisher', validators=[DataRequired()])
    synopsis = StringField('Synopsis', validators=[DataRequired()]) 

class UpdateBook(Form):
    id = HiddenField(StringField('Book ID'))
    title = StringField('Title')
    year = IntegerField('Year')
    #author = StringField('Author', validators=[DataRequired()])
    #publisher = StringField('Publisher', validators=[DataRequired()])
    synopsis = StringField('Synopsis')

class AddAuthor(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    biography = TextField('Biography', validators=[Optional()])

class UpdateAuthor(Form):
    id = HiddenField('Author ID')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    biography = TextField('Biography')

class GetAuthor(Form):
    id = HiddenField('Author ID')
    fullname = StringField('First Name')

class AddPublisher(Form):
    name = StringField('Publisher Name', validators=[DataRequired()])
    description = StringField('Publisher Description')

class UpdatePublisher(Form):
    id = HiddenField('Publisher ID')
    name = StringField('Publisher Name', validators=[DataRequired()])
    description = StringField('Publisher Description')