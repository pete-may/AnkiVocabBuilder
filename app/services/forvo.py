from __future__ import annotations
from bs4 import BeautifulSoup
from typing import List, Dict
from os import path
import os
import re
import base64
from pathlib import Path
from urllib.parse import quote, unquote
from dataclasses import dataclass

import urllib.request
from curl_cffi import requests
import tempfile

@dataclass
class Pronunciation:
    language: str
    headword: str
    query_word: str
    votes: int
    origin: str
    download_url: str
    is_ogg: bool
    id: int


class Forvo:
    def __init__(self, word, lang):
        self.url = "https://forvo.com/word/" + quote(word)
        self.pronunciations: List[Pronunciation] = []
        self.session = requests.Session()
        self.language = lang

    def get_pronunciations(self) -> Forvo:
        print("forvo.py:: fetching: ", self.url)
        res = requests.get(self.url, impersonate="chrome120")

        if res.status_code == 200:
            page = res.text
        else:
            print("forvo.py:: result code: ", res.status_code)
            print("forvo.py:: reason: ", res.reason)
            raise Exception("failed to fetch forvo page")

        html = BeautifulSoup(page, "lxml")
        available_langs_els = html.find_all(
            id="language-container-es")
        available_langs = [
            re.findall(
                r"language-container-(\w{2,4})",
                el.attrs["id"])[0] for el in available_langs_els]

        if self.language not in available_langs:
            print("forvo.py:: language not available")
            return self

        lang_container = [
            lang for lang in available_langs_els if re.findall(
                r"language-container-(\w{2,4})",
                lang.attrs["id"])[0] == self.language][0]
        pronunciations_els = lang_container.find_all(class_="pronunciations")
        pronunciation_items = pronunciations_els[0].find_all(
            class_="pronunciations-list")[0].find_all("li")

        word = self.url.rsplit('/', 2)[-1]
        headword_el = pronunciations_els[0].find_all('em')[0]
        headword = headword_el.find_all(text=True)[0].text
        headword = " ".join(headword.split()[:-2])

        for pronunciation_item in pronunciation_items:
            if len(pronunciation_item.find_all(class_="more")) == 0:
                continue
            pronunciation_dls = re.findall(
                r"Play\(\d+,'.+','.+',\w+,'([^']+)",
                pronunciation_item.find_all(
                    id=re.compile(r"play_\d+"))[0].attrs["onclick"])
            vote_count = pronunciation_item.find_all(class_="more")[0].find_all(
                class_="main_actions")[0].find_all(
                id=re.compile(r"word_rate_\d+"))[0].find_all(class_="num_votes")[0]
            vote_count_inner_span = vote_count.find_all("span")
            if len(vote_count_inner_span) == 0:
                vote_count = 0
            else:
                vote_count = int(
                    str(re.findall(r"(-?\d+).*", vote_count_inner_span[0].contents[0])[0]))
            pronunciation_dls = re.findall(
                r"Play\(\d+,'.+','.+',\w+,'([^']+)",
                pronunciation_item.find_all(
                    id=re.compile(r"play_\d+"))[0].attrs["onclick"])
            is_ogg = False
            if len(pronunciation_dls) == 0:
                pronunciation_dl = re.findall(
                    r"Play\(\d+,'[^']+','([^']+)",
                    pronunciation_item.find_all(
                        id=re.compile(r"play_\d+"))[0].attrs["onclick"])[0]
                dl_url = "https://audio00.forvo.com/ogg/" + \
                    str(base64.b64decode(pronunciation_dl), "utf-8")
                is_ogg = True
            else:
                pronunciation_dl = pronunciation_dls[0]
                dl_url = "https://audio00.forvo.com/audios/mp3/" + \
                    str(base64.b64decode(pronunciation_dl), "utf-8")
            username = pronunciation_item.find_all(
                class_="info", recursive=False)[0].find_all(
                    class_="ofLink")
            if len(username) == 0:
                for pronunciation_item_content in pronunciation_item.contents:

                    if not hasattr(pronunciation_item_content, "contents"):
                        continue

                    tempOrigin = re.findall(
                                "Pronunciation by(.*)",
                                pronunciation_item_content.contents[0],
                                re.S)

                    if len(tempOrigin) != 0:
                        origin = tempOrigin[0].strip()
                        break
            else:
                origin = username[0].contents[0].strip()
            pronunciation_object = Pronunciation(self.language,
                                                 headword,
                                                 word,
                                                 vote_count,
                                                 origin,
                                                 dl_url,
                                                 is_ogg,
                                                 -1, #data_id, can't obtain anymore
                                                 )

            self.pronunciations.append(pronunciation_object)
        return self


def fetch_audio_all(word: str, lang: str) -> Dict[str, str]:
    sounds = Forvo(word, lang).get_pronunciations().pronunciations
    if len(sounds) == 0:
        return {}
    result = {}
    for item in sounds:
        result[item.origin + "/" + item.headword] = item.download_url
    return result


def fetch_audio_best(word: str, lang: str) -> Dict[str, str]:
    sounds = Forvo(word, lang).get_pronunciations().pronunciations
    if len(sounds) == 0:
        return {}
    sounds = sorted(sounds, key=lambda x: x.votes, reverse=True)
    return {
        sounds[0].origin +
        "/" +
        sounds[0].headword: sounds[0].download_url}


def download(word, lang):
    recordings_dir = os.path.join(os.getcwd(), "app", "static", "tmp", "recordings")
    datas = fetch_audio_all(word, lang)

    for e in datas:
        page=urllib.request.Request(datas[e],headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(page).read()
        doc = requests.get(datas[e])
        e = e.replace('/', '_')
        with open(recordings_dir + "/" + e + ".mp3", "wb") as f:
            f.write(data)


if __name__ == "__main__":
    print(fetch_audio_all("delicate", "en"))
