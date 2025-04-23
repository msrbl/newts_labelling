# src/flows/train_dataset.py
from prefect import flow, task

from src.data_io.resize_images import resize_dataset

@flow(log_prints=True)
def end_to_end_dataset(ds_name: str, raw_folder: str):
    resize_and_scale(ds_name, raw_folder)
    
@task
def resize_and_scale(ds_name: str, raw_folder: str):
    """
    Resize and scale the dataset images.
    """
    resize_dataset(ds_name, raw_folder / ds_name)
    print(f"Dataset {ds_name} resized and scaled.")