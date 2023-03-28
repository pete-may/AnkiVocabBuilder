from flask import Flask
from config import Config

from flask_bootstrap import Bootstrap

import os

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app.services import anki
anki = anki.Anki()

from app.services import wiktionary
wiktionary = wiktionary.Wiktionary()

from app.services import forvo
forvo = forvo


dir_list = os.listdir(app.config["LOCAL_RECORDINGS_DIR"])
local_recording_choices = [f for f in dir_list if os.path.isfile(app.config["LOCAL_RECORDINGS_DIR"]+'/'+f)] 


image_dir_list = os.listdir(app.config["IMAGES_DIR"])
images_list = [f for f in image_dir_list if os.path.isfile(app.config["IMAGES_DIR"]+'/'+f) and ".jpg" in f] 

# print(image_dir_list)
# print(images_list)

# def setup_temp_dir():
#     if not os.path.exists(app.config["TMP_DIR"]):
#         os.makedirs(os.path.join(os.getcwd(), app.config["TEMP_DIR"]))


# def remove_temp_files():
#     for r, dirs, files in os.walk(os.path.join(os.getcwd(), app.config["TMP_DIR"]), topdown=False):
#         for name in files:
#         	# print("removing... \n" + name)
#             os.remove(os.path.join(r, name))
#         # for name in dirs:
#             # os.rmdir(os.path.join(r, name))
#             # print("removing... \n" + name)





# setup_temp_dir()
# remove_temp_files()



from app import routes

