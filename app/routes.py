from flask import render_template, url_for, request, flash, redirect
from app import app, forms

from app import local_recording_choices

from app import anki, wiktionary, forvo

from app import images_list



import re
import os


TEMP_IMAGE_CHOICES = [
    "original_size_img_14",
    "original_size_img_15",
    "original_size_img_21",
    "original_size_img_24",
    "original_size_img_28",
    "original_size_img_32"
]



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/submit', methods=['GET', 'POST'])
def index():
    form = forms.SubmitionForm()


    try:
        deck_choices = [(d, d) for d in anki.get_deck_names()]
    except:
        err = "An exception occurred. Failed to establish a connection to Anki."
        print(err) 
        return render_template("500.html", error=err), 500

    language_choices = [(l.capitalize(), l.capitalize()) for l in app.config["LANGUAGES"]]



    form.deck.choices = deck_choices
    form.language.choices = language_choices




    if form.validate_on_submit():
        language = form.language.data
        deck = form.deck.data
        word = form.word.data
        return redirect(url_for('scrape', language=language, deck=deck, word=word))





    return render_template('submit.html', form=form)


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():

    form = forms.CreateForm()

    form.recording.choices = []

    if form.validate_on_submit():
        flash(form.data)
        return redirect(url_for('index'))

    if request.method == 'POST':
        flash(form.data)
        return redirect(url_for('index'))  


    language = request.args.get('language', None)
    deck = request.args.get('deck', None)
    word = request.args.get('word', None)

    # print(language)
    # print(deck)
    # print(word)

    matches = [match for match in local_recording_choices if word in match]

    forvo.download(word)

    dir_list = os.listdir(app.config["FORVO_RECORDINGS_DIR"])
    # print(dir_list)
    forvo_recording_choices = [f for f in dir_list if os.path.isfile(app.config["FORVO_RECORDINGS_DIR"]+'/'+f)]

    # print(forvo_recording_choices) 

    wikiObject = wiktionary.search(word, language)

    

    if matches:
        form.recording.data = matches[0]

    form.recording.choices = local_recording_choices

    form.ipa.data = re.search("/.*/", wikiObject["ipa"]).group()

    return render_template('create.html', form=form, 
                                          local_recording_choices=local_recording_choices, 
                                          forvo_recording_choices=forvo_recording_choices,
                                          images=images_list)


@app.route('/create', methods=['POST'])
def create():
    form = forms.CreateForm()
    if not form.validate_on_submit():
        flash('Validation FAILED.\nError:\n{}'.format(form.errors))
        return redirect('/submit', code=307)
    else:
        flash('Scrape request created.\nData:\n{}'.format(form.data))



@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)






