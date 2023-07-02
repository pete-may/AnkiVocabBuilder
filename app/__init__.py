import os

from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app.services import anki
from app.services.google_images import GoogleImages
from app.services import forvo
from app.services import wiktionary
from app.services import google_images

anki = anki.Anki()
forvo = forvo
google_images = google_images.GoogleImages(app.config["SERP_API_KEY"])
wiktionary = wiktionary.Wiktionary()

def setup_temp_dir():
    if not os.path.exists(app.config["TMP_DIR"]):
        os.makedirs(os.path.join(os.getcwd(), app.config["TMP_DIR"]))

def remove_temp_recordings():
    for r, dirs, files in os.walk(os.path.join(os.getcwd(), app.config["RECORDINGS_DIR"]), topdown=False):
        for name in files:
            os.remove(os.path.join(r, name))

def remove_temp_images():
    for r, dirs, files in os.walk(os.path.join(os.getcwd(), app.config["IMAGES_DIR"]), topdown=False):
        for name in files:
            os.remove(os.path.join(r, name))

setup_temp_dir()
remove_temp_recordings()
remove_temp_images()

from app import routes

