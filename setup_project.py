import deeplabcut

from src.config import ROOT_FOLDER

videos = []

deeplabcut.create_new_project(
    "DLC-Project", 
    "exp", 
    videos, 
    working_directory=ROOT_FOLDER, 
    multianimal=False)