from pathlib import Path
from prefect import flow, task
from src.data_io.drive.drive_manager import list_tar_files, download_tar_file, upload_tar_file
import tarfile
import shutil
import subprocess
import os
import re

from src.config import DATA_FOLDER, PROCESSED_FOLDER_ID
import json
import io

@task
def get_datasets_to_upload() -> list[dict]:
    processed_archives = list_tar_files(PROCESSED_FOLDER_ID)
    
    new_archives = []
    for dataset in os.listdir(DATA_FOLDER / "processed"):
        if dataset not in [archive['name'] for archive in processed_archives]:
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

    upload_tar_file(tar_file_path, PROCESSED_FOLDER_ID)
    
    os.remove(tar_file_path)

@flow(log_prints=True)
def upload_processed_datasets(processed_folder: Path):
    datasets = get_datasets_to_upload()
    if not datasets:
        print("No new archives found.")
        return
    
    for dataset in datasets:
        pack_and_upload(dataset, processed_folder)
        print(f"Packed and uploaded {dataset}")