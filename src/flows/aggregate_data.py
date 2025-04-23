# src/flows/train_dataset.py
from pathlib import Path
from prefect import flow, task

from src.data_io.resize_images import resize_dataset

@flow(log_prints=True)
def end_to_end_dataset(dataset_path: Path):
    resize_and_scale(dataset_path)
    
@task
def resize_and_scale(dataset_path: Path):
    """
    Resize and scale the dataset images.
    """
    resize_dataset(dataset_path)
    print(f"Dataset {dataset_path} resized and scaled.")