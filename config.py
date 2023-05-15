import os


class Config(object):
    APP_TITLE = "Anki Vocab Builder"
    SECRET_KEY = "my-anki-vocab-builder"
    # REMOVE ME
    LOCAL_RECORDINGS_DIR = os.path.join(os.getcwd(), "app", "static", "recordings")
    FORVO_RECORDINGS_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "recordings")
    IMAGES_DIR = os.path.join(os.getcwd(), "app", "static", "tmp", "images")
    TMP_DIR = os.path.join(os.getcwd(), "app", "static", "tmp")
    LANGUAGES = ["spanish"]
    NOTE_TYPE = "Vocab Word"
    SERP_API_KEY = "e0b8acf5676704931d1250c44c7804888151da32f83a99cf05151621ad7b4a5d"
    DEFAULT_DECK = "Spanish::Vocab"
