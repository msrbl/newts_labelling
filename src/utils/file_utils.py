import os
from pathlib import Path


def get_image_and_json_paths(target_folder: Path):
    image_paths = []
    json_paths = []
    
    for root, dirs, files in os.walk(target_folder):
        for d in dirs:
            if d == "images":
                image_paths.append(os.path.join(root, d))
        for file in files:
            if file == "instances.json":
                json_paths.append(os.path.join(root, file))
                
    return image_paths, json_paths