import requests
import os
import base64
import html

from app import app

class Anki:
    URL = "http://localhost:8765/"
    VERSION = 6

    def __init__(self):
        pass

    def invoke(self, action, params=None):
        payload = {"action": action, "version": self.VERSION}
        if params:
            payload["params"] = params
        response = requests.request("POST", self.URL, json=payload).json()
        if len(response) != 2:
            raise Exception("response has an unexpected number of fields")
        if "error" not in response:
            raise Exception("response is missing required error field")
        if "result" not in response:
            raise Exception("response is missing required result field")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def get_deck_names(self):
        return self.invoke("deckNames")

    def store_media_file(self, src_file_path, word):
        action = "storeMediaFile"
        sanitized_word = "".join([c for c in word if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        ext = os.path.splitext(src_file_path)[1]
        dst = "{}{}".format(sanitized_word, ext)

        with open(src_file_path, 'rb') as f:
            b64_output = base64.b64encode(f.read()).decode('utf-8')
        params = {
            "filename": dst,
            "data": b64_output
        }

        self.invoke(action, params)
        return dst


    @staticmethod
    def format_notes(notes):
        html_notes = "<br>".join(html.escape(notes.strip()).split("\n"))
        return "<div>{}</div>".format(html_notes)

    def add_note(self, deck_name, word, image_paths, recording_file_path, recording_type, ipa_text, gender, notes):
        stored_images = []
        for i, image_path in enumerate(image_paths):
            print("image_path")
            print(image_path)
            image_path_path = app.config["IMAGES_DIR"] + '/' + image_path
            print(image_path_path)
            stored_images.append(self.store_media_file(image_path_path, "{}-{}".format(word, i)))

        picture_field = ""
        for stored_image in stored_images:
            picture_field += '<img src="{}">'.format(stored_image)

        formatted_notes = self.format_notes(notes)

        # pronunciation_field = ipa_text

        if recording_file_path:
            print("recording_path")
            print(recording_file_path)
            print(recording_type)
            recording_file_path_path = ''
            if recording_type == 'local':
                recording_file_path_path = app.config["LOCAL_RECORDINGS_DIR"] + '/' + recording_file_path
            else:
                recording_file_path_path = app.config["FORVO_RECORDINGS_DIR"] + '/' + recording_file_path
            print(recording_file_path_path)
            stored_audio_filename = self.store_media_file(recording_file_path_path, word)
            pronunciation_field = "[sound:{}]".format(stored_audio_filename)

        gender_selection = ''
        if gender == 'male':
            gender_selection = 'm'
        elif gender == 'female':
            gender_selection = 'f'
        elif gender == 'either':
            gender_selection = 'e'

        params = {
            "note": {
                "deckName": deck_name,
                "modelName": app.config["NOTE_TYPE"],
                "fields": {
                    "Word": word,
                    "Picture": picture_field,
                    "Recording": pronunciation_field,
                    "IPA": ipa_text,
                    "Gender (m/f/e)": gender_selection,
                    "Notes": formatted_notes
                },
                "tags": []
            }
        }

        note_id = self.invoke("addNote", params)
        return note_id

