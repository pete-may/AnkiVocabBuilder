import os


class Config(object):
    APP_TITLE = "Anki Vocab Builder"
    SECRET_KEY = "my-anki-vocab-builder"
    LOCAL_RECORDINGS_DIR = os.path.join(os.getcwd(), "app", "static", "recordings")
    FORVO_RECORDINGS_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "recordings")
    IMAGES_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "images")
    LANGUAGES = ["spanish"]
