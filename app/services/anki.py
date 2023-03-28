import requests

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