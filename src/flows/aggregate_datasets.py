from pathlib import Path
from prefect import flow, task

from src.config import RAW_FOLDER
from src.services.resize_dataset import resize_dataset
    
@task
def resize_and_scale(dataset_path: Path):
    """
    Resize and scale the dataset images.
    """
    resize_dataset(dataset_path)
    
@flow(log_prints=True)
def end_to_end_dataset():
    for dataset in RAW_FOLDER.iterdir():
        resize_and_scale(dataset)
    
if __name__=="__main__":
    end_to_end_dataset()