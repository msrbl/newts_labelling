from pathlib import Path
from prefect import flow, task
from src.services.drive.drive_manager import list_tar_files, upload_tar_file
import tarfile
import os

from src.config import DATA_FOLDER, DRIVE_PROCESSED_FOLDER_ID, PROCESSED_FOLDER

@task
def get_datasets_to_upload() -> list[dict]:
    processed_archives = list_tar_files(DRIVE_PROCESSED_FOLDER_ID)
    
    new_archives = []
    for dataset in os.listdir(DATA_FOLDER / "processed"):
        if dataset not in [archive['name'].split('.')[0] for archive in processed_archives]:
            new_archives.append(dataset)
    
    return new_archives

@task
def pack_and_upload(ds_name: str, folder: Path):
    """
    Pack the dataset into a tar file and upload it to Google Drive.
    """
    tar_file_path = folder / f"{ds_name}.tar"
    
    with tarfile.open(tar_file_path, "w") as tar:
        tar.add(folder / ds_name, arcname=os.path.basename(ds_name))

    upload_tar_file(tar_file_path, DRIVE_PROCESSED_FOLDER_ID)
    
    os.remove(tar_file_path)

@flow(log_prints=True)
def upload_processed_datasets():
    datasets = get_datasets_to_upload()
    if not datasets:
        print("No new archives found.")
        return
    
    for dataset in datasets:
        pack_and_upload(dataset, PROCESSED_FOLDER)
        print(f"Packed and uploaded {dataset}")
        
if __name__ == "__main__":
    upload_processed_datasets()