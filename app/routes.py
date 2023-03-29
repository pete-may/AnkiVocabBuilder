from flask import render_template, url_for, request, flash, redirect, jsonify
from app import app, forms

from app import local_recording_choices

from app import anki, wiktionary, forvo

from app.services.google_images import serpapi_get_google_images

from app import remove_temp_recordings, remove_temp_images

import re
import os



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

        print(form.recording_type.data)

        anki.add_note(form.deck.data, 
                      form.word.data,
                      form.images.data.split(","),
                      form.recording.data,
                      form.recording_type.data,
                      form.ipa.data,
                      form.gender.data,
                      form.notes.data
                      )


        return redirect(url_for('index'))

    if request.method == 'POST':
        flash(form.data)
        flash(form.errors)
        return redirect(url_for('index'))  

    root = word

    remove_temp_recordings()
    remove_temp_images()
    setup_root_dir(root)

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

    serpapi_get_google_images(root, word, 0)

    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f]

    form.deck.data = deck
    form.word.data = word
    form.search_query.data = word

    form.gender.data = 'none'
    
    if matches:
        form.recording.data = matches[0]

    form.recording.choices = [(c,c) for c in local_recording_choices]
    form.recording_type.data = 'local'

    form.ipa.data = re.search("/.*/", wikiObject["ipa"]).group()

    return render_template('create.html', form=form, 
                                          query=word,
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


@app.route('/get_more_images')
def get_more_images():
    root = request.args.get('root')
    query = request.args.get('query')
    offset = request.args.get('offset')
    refresh_images = request.args.get('refresh_images')
    print ("Hello")
    print (query)
    print (offset)
    print (refresh_images)

    if refresh_images.lower() == 'true':
        print ("deleting")
        remove_temp_images()
    else:
        print ("not deleting")


    serpapi_get_google_images(root, query, int(offset))
    image_dir_list = os.listdir(app.config["IMAGES_DIR"])
    images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f] 

    return jsonify(images_list)






