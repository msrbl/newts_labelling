from pathlib import Path
import shutil
import deeplabcut

import yaml

from src.config import PROCESSED_FOLDER, ROOT_FOLDER
from prefect import flow, task

from src.deeplabcut.labels import create_csv_in_subfolders
from src.utils import get_image_and_json_paths
from src.utils.structured_data import build_skeleton

@task(log_prints=False)
def create_project(project_name, experimenter, image_paths):
    """
    Create a new DeepLabCut project.
    :param project_name: Name of the project
    :param experimenter: Your name (or experimenter)
    :param video_paths: List of paths to video files
    :return: Path to the config file created by DeepLabCut
    """
    
    for item in ROOT_FOLDER.iterdir():
        if item.is_dir() and item.name.startswith(project_name):
            print(f"Project {project_name} already exists.")
            yaml_file = next(item.glob("*.yaml"), None)
            if yaml_file is not None:
                return str(yaml_file)
            print("No .yaml file found in the existing project folder.")
            return None
    
    config_path = deeplabcut.create_new_project(
        project_name, 
        experimenter, 
        image_paths, 
        working_directory=ROOT_FOLDER, 
        copy_videos=True
    )
    print(f"Created project with config: {config_path}")
    
    extract_frames(config_path)
    return config_path

@task(log_prints=False)
def extract_frames(config_path):
    """
    Automatically extract frames from the videos using a k-means approach.
    """
    deeplabcut.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False)
    print("Frames extraction completed.")
    
@task
def fill_labeled_data(config_path: str, paths: list[str], labeled_dir: Path):
    create_csv_in_subfolders(paths, labeled_dir)
    
    deeplabcut.convertcsv2h5(config_path, userfeedback=False)

@task
def pack_project_zip(directory: Path):
    """
    Pack the project into a zip file.
    """
    project_name = directory.name
    zip_path = directory.with_suffix('.zip')
    
    if zip_path.exists():
        zip_path.unlink()
    
    shutil.make_archive(project_name, 'zip', directory)
    print(f"Packed project into: {zip_path}")
    
    shutil.rmtree(directory)
    print(f"Removed directory: {directory}")

@task
def change_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    project_name = Path(config_path).parent.name
    config['project_path'] = f"\\content"

    for old_key in list(config['video_sets'].keys()):
        file_name = old_key.split("\\")[-1]
        new_key = f"{config['project_path']}\\videos\\{file_name}"

        config['video_sets'][new_key] = config['video_sets'].pop(old_key)
                
    config['batch_size'] = 4
    config['bodyparts'] = [f"point{i}" for i in range(1, 22)]
    config['numframes2pick'] = 1
    config['skeleton'] = build_skeleton()

    with open(config_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False)

    print("Конфигурация успешно обновлена!")

@flow(log_prints=True)
def initialize_dlc_project():
    project_name = 'DLC-Project'
    experimenter = 'exp'
    
    image_paths, json_paths = get_image_and_json_paths(PROCESSED_FOLDER)
                
    config_path = create_project(project_name, experimenter, image_paths)
    
    if config_path:
        project_root_dir = Path(config_path).parent
        
        labeled_dir = project_root_dir / "labeled-data"
        fill_labeled_data(config_path, json_paths, labeled_dir)
        
        change_config(config_path)
        
        pack_project_zip(project_root_dir)
        
if __name__ == "__main__":
    initialize_dlc_project()