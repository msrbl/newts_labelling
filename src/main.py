from pathlib import Path
import shutil
from prefect import flow, task
import argparse


from src.config import DATA_FOLDER, PROCESSED_FOLDER, RAW_FOLDER

from src.flows.initialize_project import initialize_dlc_project
from src.flows.upload_datasets import upload_processed_datasets
from src.flows.raw_datasets import get_raw_datasets
from src.flows.aggregate_data import end_to_end_dataset

@task
def cleanup(path: Path):
    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
            print(f"Deleted directory: {item}")

@flow(log_prints=True)
def start_flow(upload_flag: bool = True, initialize_flag: bool = True):
    """
    This is the main pipeline that orchestrates the loading of raw datasets and their processing.
    """
    try:   
        datasets = get_raw_datasets()
        if not datasets:
            print("No datasets found.")
        else:
            for dataset in datasets:
                end_to_end_dataset(RAW_FOLDER / dataset['name'])

            cleanup(RAW_FOLDER)
            
            if upload_flag:
                upload_processed_datasets()
            
            if initialize_flag:
                initialize_dlc_project()
            
            cleanup(PROCESSED_FOLDER)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DeepLabCut project initialization and dataset processing")
    # parser.add_argument("dataset_dir", type=Path, help="Path to folder with datasets in COCO format")
    parser.add_argument("--no-upload", action="store_true", help="Whether to skip uploading the processed datasets")
    parser.add_argument("--no-initialize", action="store_true", help="Whether to skip initializing the DeepLabCut project")

    args = parser.parse_args()
    start_flow(not args.no_upload, not args.no_initialize)