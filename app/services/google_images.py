import json
import urllib.request
import urllib.error
from urllib.parse import urlencode, quote_plus

import redis

from serpapi import GoogleSearch
from unidecode import unidecode

redis_client = redis.Redis()

BATCH_SIZE = 6
SKIP_INDEXES = []


class GoogleImages:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_images(self, query, offset=0):
        image_results = []
        results = {}

        search_id = ""
        REDIS_RUNNING = True
        try:
            search_id = redis_client.get(query)
        except redis.exceptions.ConnectionError:
            REDIS_RUNNING = False
            print("Warning: The Redis server is not running. Searches will not be saved.")

        if search_id:
            search_id = search_id.decode("utf-8")
            print("found past search: " + search_id)
            results = GoogleSearch({"api_key": self.api_key}).get_search_archive(search_id, 'json')
        else:
            print("no past search found, starting new search")

            # search query parameters
            params = {
                "engine": "google",
                "q": query,
                "tbm": "isch",
                "api_key": self.api_key,
                "tbs": "isz:m"
            }

            search = GoogleSearch(params)         # where data extraction happens
            results = search.get_dict()       # JSON -> Python dictionary

            new_search_id = results.get("search_metadata").get("id")
            print("search id:")
            print(new_search_id)

            if REDIS_RUNNING:
                redis_client.set(query, new_search_id)

        # Downloading images

        if not results:
            print("google_images.py:: whoops, no results found")
            return

        for index, image in enumerate(results["images_results"]):

            if index in SKIP_INDEXES:
                continue

            if index < offset*BATCH_SIZE:
                continue

            if index >= (offset*BATCH_SIZE)+BATCH_SIZE:
                return

            if not image.get("original"):
                print("No image['original'], skipping...")
                continue

            print(f"Downloading {index} image...")

            try:
                opener=urllib.request.build_opener()
                opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
                urllib.request.install_opener(opener)

                urllib.request.urlretrieve(image["original"], f"app/static/tmp/images/{query}_img_{index}.jpg")
            except urllib.error.URLError:
                print(f"Downloading {index} image FAILED - 404")


