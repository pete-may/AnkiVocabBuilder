from flask import render_template, url_for, request, flash, redirect, jsonify
from app import app, forms, anki, wiktionary, forvo, get_images
from app import local_recording_choices
from app import remove_temp_recordings, remove_temp_images

import re
import os



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/submit', methods=['GET', 'POST'])
def index():
    form = forms.SubmitForm()

    language_choices = [(l.capitalize(), l.capitalize()) for l in app.config["LANGUAGES"]]
    try:
        deck_choices = [(d, d) for d in anki.get_deck_names()]
    except:
        err_msg = "An exception occurred. Failed to establish a connection to Anki."
        return render_template("500.html", error=err_msg), 500


    form.language.choices = language_choices
    form.deck.choices = deck_choices

    # default deck
    form.deck.data = "Spanish::Vocab"

    if form.validate_on_submit():
        language = form.language.data
        deck = form.deck.data
        word = form.word.data
        return redirect(url_for('create', language=language, deck=deck, word=word))

    return render_template('submit.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():

    form = forms.CreateForm()

    form.recording.choices = []

    if form.validate_on_submit():
        # flash(form.data)
        try:
            anki.add_note(form.deck.data,
                          form.word.data,
                          form.images.data.split(","),
                          form.recording.data,
                          form.recording_type.data,
                          form.ipa.data,
                          form.gender.data,
                          form.notes.data
                          )
        except Exception as e:
            if 'duplicate' in str(e):
                err_msg = "An exception occurred. Duplicate card found in Anki."
                return render_template("500.html", error=err_msg), 500
            else:
                return render_template("500.html", error=e), 500

        return redirect(url_for('index'))

    # request is a POST and it didn't pass validation; return to index
    if request.method == 'POST':
        # flash(form.data)
        # flash(form.errors)
        return redirect(url_for('index'))  

    # cleanup tmp folders
    remove_temp_recordings()
    remove_temp_images()

    language = request.args.get('language', None)
    deck = request.args.get('deck', None)
    word = request.args.get('word', None)

    # autofill gender selection
    words = word.split()
    if 'el' in words:
        words = [w for w in words if w != 'el']
        word = ' '.join(words)
        form.gender.data = 'male'
    elif 'la' in words:
        words = [w for w in words if w != 'la']
        word = ' '.join(words)
        form.gender.data = 'female'
    else:
        form.gender.data = 'none'

    # print(language)
    # print(deck)
    # print(word)

    form.deck.data = deck
    form.word.data = word
    form.search_query.data = word

    # scrape all the things
    get_images(word, 0)
    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f]

    form.recording.choices = [(c,c) for c in local_recording_choices]
    form.recording_type.data = 'local'

    matches = [match for match in local_recording_choices if word in match]
    if matches:
        form.recording.data = matches[0]

    forvo.download(word)
    dir_list = os.listdir(app.config["FORVO_RECORDINGS_DIR"])
    forvo_recording_choices = [f for f in dir_list if os.path.isfile(app.config["FORVO_RECORDINGS_DIR"]+'/'+f)]

    wikiObject = wiktionary.search(word, language)
    if wikiObject.get("ipa"):
        form.ipa.data = re.search("/.*/", wikiObject["ipa"]).group()

    return render_template('create.html', form=form, 
                                          query=word,
                                          local_recording_choices=local_recording_choices, 
                                          forvo_recording_choices=forvo_recording_choices,
                                          images=images_list)


@app.route('/get_more_images')
def get_more_images():
    query = request.args.get('query')
    offset = request.args.get('offset')
    refresh_images = request.args.get('refresh_images')

    print(refresh_images)
    # if refresh_images.lower() == 'true':
    #     remove_temp_images()

    get_images(query, int(offset))
    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f] 

    return jsonify(images_list)


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)






