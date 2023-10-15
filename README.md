# AnkiVocabBuilder

AnkiVocabBuilder is a language learning tool that helps you easily generate a deck of Anki flashcards to learn vocab words in your target language.

Submit a word and and it provides a simple interface that lets you select image and audio files to add to your flashcards.

When your finished, click Add to Anki, and the card will be inserted into your language deck.

### Demo

![AnkiVocabBuilder Demo](https://github.com/pete-may/AnkiVocabBuilder/assets/16448655/e8fe68e1-bbbb-4eb0-b5e4-23f7b40ac3c5)

### Media Sources

- Images - Google Images via [SerpAPI](https://serpapi.com/)
- Pronunciation - [Forvo](https://forvo.com/)
- IPA - [Wiktionary](https://www.wiktionary.org/)

## Prerequisites

#### 1. [Download Anki](https://apps.ankiweb.net/)

#### 2. [Install AnkiConnect](https://ankiweb.net/shared/info/2055492159)

#### 3. Download the template deck
I've provided a template deck that you can use to get started.

Go to <https://ankiweb.net/shared/info/1737709539> and click "Download" to download the deck. Then import it into Anki.

This deck contains a note type that AnkiVocabBuilder uses to create new cards. You can customize this note type to your liking.

**Note:** I've added a short script to the Back Template of my Anki cards that dynamically adds Spanish definite articles to gendered nouns. For example, entering 'm' in the gender field for "gato" renders the word as "el gato" during study. Feel free to change this to your target language's definite articles or to not use the feature at all.

#### 4. Create a SerpAPI account
This app uses SerpAPI to get images from Google Images. You'll need to create an account to use this app. There's a free tier that allows you to make 100 searches per month.

Go to <https://serpapi.com/> and create an account. You will need to [add your SerpAPI secret key to the config file.](#3-add-your-serpapi-secret-key-to-the-config-file)

#### 5. Download Redis (optional)
The free version of SerpAPI limits the number of searches you can do per month. To help avoid hitting this limit on repeat searches, AnkiVocabBuilder caches SerpAPI search ids in a locally running Redis database. If you don't want to use Redis, simply don't install it.

## Installing

#### 1. Clone this repository and change into the directory

```code
git clone https://github.com/pete-may/AnkiVocabBuilder.git
cd AnkiVocabBuilder
```

#### 2. Create a virtual environment and install all of the dependencies

```code
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

#### 3. Add your SerpAPI secret key to the [config file](./config.py#L11)

```
    SERP_API_KEY = <YOUR_KEY_HERE>
```

#### 4. Install Redis to cache SerpAPI search ids (optional)

macOS:
```code
brew install redis
```

## Usage

#### 1. Make sure Anki is running

#### 2. Start Redis server (optional):
```code
brew services start redis
```

#### 3. Run:

```code
flask run
```

#### 4. Go to <http://localhost:5000/> in your browser.

## Misc.

### Adding a language

To add a new language, add the language name and its [lanuage code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) to the [config file](./config.py#L9):

```
    LANGUAGES = {"Spanish": "es", "French": "fr", "Russian": "ru"}
```

## Acknowledgements

- The philosophy behind this app comes from the Fluent Forever method: <https://blog.fluent-forever.com/gallery/>
- This design of this app was based off of this project: <https://github.com/cofinley/FluentForeverVocabBuilder>
- The Forvo implementation came from: <https://github.com/FreeLanguageTools/vocabsieve>
- This tutorial taught me a lot about Flask: <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world>
