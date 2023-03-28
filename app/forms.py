from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class SubmitionForm(FlaskForm):
    language = SelectField("Language", validators=[DataRequired()])
    deck = SelectField("Deck", validators=[DataRequired()])
    word = StringField("Word", validators=[DataRequired()])
    submit = SubmitField("Submit", id="submit_submit")


class CreateForm(FlaskForm):
    ipa = StringField("IPA", validators=[DataRequired()])
    recording = SelectField("Recording", validators=[DataRequired()])
    # forvo_recording = SelectField("Forvo recording", validators=[DataRequired()])
    # recordings = StringField("Recordings", validators=[DataRequired()])
    # recording = StringField("Recording", validators=[DataRequired()])
    # word_usage = SelectField("Word Usage")
    # image_query = StringField("Image Query")
    images = HiddenField("Images")
    notes = TextAreaField("Notes")
    # test_spelling = BooleanField("Test Spelling?")
    submit = SubmitField("Add to Anki", id="create_submit")
