import json
import urllib.request
import urllib.error

import redis

from serpapi import GoogleSearch
from unidecode import unidecode

redis_client = redis.Redis()
BATCH_SIZE = 6

def serpapi_get_google_images(query, offset=0):
    image_results = []
    results = {}

    search_id = redis_client.get(query)

    if search_id:
        search_id = search_id.decode("utf-8")
        print("found past search: " + search_id)
        results = GoogleSearch({"api_key": "e0b8acf5676704931d1250c44c7804888151da32f83a99cf05151621ad7b4a5d"}).get_search_archive(search_id, 'json')
    else:
        print("no past search found, starting new search")

        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                    # search query
            "tbm": "isch",                    # image results
            "api_key": "",
            "tbs": "isz:m",
            "hl": "es"
        }

        search = GoogleSearch(params)         # where data extraction happens
        results = search.get_dict()       # JSON -> Python dictionary
        

        new_search_id = results.get("search_metadata").get("id")
        print("search id:")
        print(new_search_id)
        redis_client.set(query, new_search_id)

    # Downloading images

    for index, image in enumerate(results["images_results"]):

        if index < offset*BATCH_SIZE:
            continue

        if index >= (offset*BATCH_SIZE)+BATCH_SIZE:
            return

        if not image.get("original"):
            print("No image['original'], skipping...")
            continue

        print(f"Downloading {index} image...")

        query = unidecode(query)

        try:
            opener=urllib.request.build_opener()
            opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(image["original"], f"app/static/tmp/images/{query}_img_{index}.jpg")
        except urllib.error.URLError:
            print(f"Downloading {index} image FAILED - 404")
        




