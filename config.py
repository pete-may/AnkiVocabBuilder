import os

class Config(object):
    APP_TITLE = "Anki Vocab Builder"
    SECRET_KEY = "my-anki-vocab-builder"
    RECORDINGS_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "recordings")
    IMAGES_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "images")
    TMP_DIR = os.path.join(os.getcwd(), "app", "static", "tmp")
    LANGUAGES = {"Spanish": "es", "French": "fr", "Russian": "ru"}
    NOTE_TYPE = "Vocab Word"
    SERP_API_KEY = "<YOUR_KEY_HERE>"
    DEFAULT_DECK = "Spanish::Vocab"

