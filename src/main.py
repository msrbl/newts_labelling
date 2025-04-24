from pathlib import Path
import shutil
from prefect import flow, task

from src.config import DATA_FOLDER, PROCESSED_FOLDER, RAW_FOLDER
import json

from src.flows.init_dlc_project import initialize_dlc_project
from src.flows.upload_datasets import upload_processed_datasets
from src.flows.download_raw_archives import load_raw_dataset
from src.flows.aggregate_datasets import end_to_end_dataset

@task
def cleanup(path: Path):
    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
            print(f"Deleted directory: {item}")

@flow(log_prints=True)
def start_flow():
    """
    This is the main pipeline that orchestrates the loading of raw datasets and their processing.
    """
    try:   
        
        datasets = load_raw_dataset()
        if datasets is None:
            print("No new datasets found.")
        else:
            for dataset in datasets:
                end_to_end_dataset(RAW_FOLDER / dataset['name'])

            cleanup(RAW_FOLDER)
                
            upload_processed_datasets()
            
            initialize_dlc_project()
            
            cleanup(PROCESSED_FOLDER)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
        
if __name__ == "__main__":
    start_flow()