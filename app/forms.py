from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired

class SubmitionForm(FlaskForm):
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
    recording_type = HiddenField("Recording Type")
    ipa = StringField("IPA", validators=[DataRequired()])
    gender = RadioField("Gender", choices=[('none', 'None'), ('male','Male'),('female','Female'), ('either', 'Either')])
    notes = TextAreaField("Notes")
    submit = SubmitField("Add to Anki", id="create_submit")
