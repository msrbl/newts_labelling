import shutil
from prefect import flow, task

from src.config import DATA_FOLDER
import json

from src.flows.upload_datasets import upload_processed_datasets
from src.flows.load_raw_archives import load_raw_dataset
from src.flows.aggregate_data import end_to_end_dataset

RAW_FOLDER = DATA_FOLDER / "raw"
PROCESSED_FOLDER = DATA_FOLDER / "processed"

@task
def cleanup_raw(ds_name: str):
    dataset_path = RAW_FOLDER / ds_name
    if dataset_path.exists():
        shutil.rmtree(dataset_path)
        print(f"Removed raw dataset directory: {dataset_path}")
    else:
        print(f"Raw dataset directory does not exist: {dataset_path}")

@flow(log_prints=True)
def start_flow():
    """
    This is the main pipeline that orchestrates the loading of raw datasets and their processing.
    """
    try:
        processed_datasets_file = DATA_FOLDER / "processed_datasets.json"
        if not processed_datasets_file.exists():
            with open(processed_datasets_file, "w") as f:
                data = []
                json.dump(data, f, indent=4)
                
        
        datasets = load_raw_dataset(RAW_FOLDER)
        if datasets is None:
            print("No new datasets found.")
        
        for dataset in datasets:
            end_to_end_dataset(RAW_FOLDER / dataset['name'])
        
            with open(processed_datasets_file, "r") as f:
                data = json.load(f)
                
            if dataset not in data:
                data.append(dataset)
                with open(processed_datasets_file, "w") as f:
                    json.dump(data, f, indent=4)
                    
            cleanup_raw(dataset['name'])
            
        upload_processed_datasets(PROCESSED_FOLDER)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
        
if __name__ == "__main__":
    start_flow()