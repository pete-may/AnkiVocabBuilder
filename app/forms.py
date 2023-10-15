from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired

class SubmitForm(FlaskForm):
    language = SelectField("Language", validators=[DataRequired()])
    deck = SelectField("Deck", validators=[DataRequired()])
    word = StringField("Word", validators=[DataRequired()])
    submit = SubmitField("Submit", id="submit_submit")

class CreateForm(FlaskForm):
    deck = HiddenField("Deck", validators=[DataRequired()])
    word = HiddenField("Word", validators=[DataRequired()])
    images = HiddenField("Images")
    search_query = HiddenField("Search Query")
    recording = SelectField("Recording", validate_choice=False)
    ipa = StringField("IPA")
    gender = RadioField("Gender", choices=[('none', 'None'), ('masculine','Masculine'), ('feminine','Feminine')])
    notes = TextAreaField("Notes")
    submit = SubmitField("Add to Anki", id="create_submit")
