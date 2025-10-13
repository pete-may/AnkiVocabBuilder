from wiktionaryparser import WiktionaryParser

class Wiktionary:
    def __init__(self):
        self.parser = WiktionaryParser()

    def search(self, query, language):
        self.parser.language = language
        res = self.parser.fetch(query)
        if not isinstance(res, list):
            print("Wiktionary search failed. No results found.")
            return None

        query = res[0]
        pronunciation = query["pronunciations"]
        if len(pronunciation["text"]):
            ipa = pronunciation["text"][0].replace("IPA: ", "")
        else:
            ipa = ""

        audio_filename = ""
        definition_choices = [(d["partOfSpeech"], d["text"][0]) for d in query["definitions"]]
        return {
            "ipa": ipa,
            "audio_filename": audio_filename,
            "definitions": definition_choices
        }
