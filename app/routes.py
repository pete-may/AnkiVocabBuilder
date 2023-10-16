from flask import render_template, url_for, request, redirect, jsonify, flash
from app import app, forms, anki, wiktionary, forvo, google_images
from app import remove_temp_recordings, remove_temp_images

import re
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/submit', methods=['GET', 'POST'])
def index():
    form = forms.SubmitForm()
    language_choices = [(l, l) for l in app.config["LANGUAGES"].keys()]

    try:
        deck_choices = [(d, d) for d in anki.get_deck_names()]
    except:
        err_msg = "An exception occurred. Failed to establish a connection to Anki."
        print(err_msg)
        return render_template("500.html", error=err_msg), 500

    form.language.choices = language_choices
    form.deck.choices = deck_choices

    # default deck
    if not form.deck.data:
        form.deck.data = app.config["DEFAULT_DECK"]

    if form.validate_on_submit():
        language = form.language.data
        deck = form.deck.data
        word = form.word.data.lower()
        return redirect(url_for('create', language=language, deck=deck, word=word))

    return render_template('submit.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateForm()
    form.recording.choices = []

    if form.validate_on_submit():
        try:
            anki.add_note(form.deck.data,
                          form.word.data,
                          form.images.data.split(","),
                          form.recording.data,
                          form.ipa.data,
                          form.gender.data,
                          form.notes.data
                          )
            flash("Card added successfully!")
        except Exception as e:
            if 'duplicate' in str(e):
                err_msg = "An exception occurred. Duplicate card found in Anki."
                print(err_msg)
                return render_template("500.html", error=err_msg), 500
            else:
                return render_template("500.html", error=e), 500

        return redirect(url_for('index'))

    # request is a POST and it didn't pass validation; return to index
    if request.method == 'POST':
        return redirect(url_for('index'))

    # cleanup tmp folders
    remove_temp_recordings()
    remove_temp_images()

    language = request.args.get('language', None)
    deck = request.args.get('deck', None)
    word = request.args.get('word', None)

    # autofill gender selection (Spanish only)
    words = word.split()
    if 'el' in words:
        words = [w for w in words if w != 'el']
        word = ' '.join(words)
        form.gender.data = 'masculine'
    elif 'la' in words:
        words = [w for w in words if w != 'la']
        word = ' '.join(words)
        form.gender.data = 'feminine'
    else:
        form.gender.data = 'none'

    form.deck.data = deck
    form.word.data = word
    form.search_query.data = word

    ### scrape all the things

    # recordings
    # do forvo first so we can fail if the word doesn't exist
    try:
        forvo.download(word, app.config["LANGUAGES"][language])
    except Exception as e:
        print(e)
        err_msg = "A Forvo exception occurred."
        return render_template("500.html", error=err_msg), 500

    recordings_dir_list = os.listdir(app.config["RECORDINGS_DIR"])
    recording_choices = [f for f in recordings_dir_list if os.path.isfile(app.config["RECORDINGS_DIR"] + '/' + f)]
    form.recording.choices = [(c,c) for c in recording_choices]

    # images
    google_images.get_images(word, 0)
    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"] + '/' + f) and ".jpg" in f]

    # ipa
    wikiObject = wiktionary.search(word, language)
    if wikiObject.get("ipa"):
        match = re.search("/.*/", wikiObject["ipa"])
        if match:
            form.ipa.data = match.group()
        else:
            match = re.search("\[.*\]", wikiObject["ipa"])
            if match:
                form.ipa.data = match.group()

    return render_template('create.html', form=form,
                                          query=word,
                                          images=images_list)


# search for extra images within the current query
@app.route('/get_more_images')
def get_more_images():
    query = request.args.get('query')
    offset = request.args.get('offset')
    refresh_images = request.args.get('refresh_images')

    google_images.get_images(query, int(offset))
    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f]

    return jsonify(images_list)


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

