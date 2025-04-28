import os
from pathlib import Path
from prefect import flow, task
from src.services.drive.drive_manager import list_tar_files, download_tar_file
import tarfile
import shutil
import re

from src.config import DRIVE_PROCESSED_FOLDER_ID, DRIVE_RAW_FOLDER_ID, RAW_FOLDER, ROOT_FOLDER, SERVICE_ACCOUNT_FILE

from src.services.merge_files import merge_subfolders

@task
def get_new_archives() -> list[dict]:
    raw_archives = list_tar_files(DRIVE_RAW_FOLDER_ID)
    processed_datasets = list_tar_files(DRIVE_PROCESSED_FOLDER_ID)

    pattern = r"^(?P<name>[^/]+)\.tar$"
    new_archives = []
    for archive in raw_archives:
        match = re.match(pattern, archive['name'])
        if match and archive['name'] not in [a['name'] for a in processed_datasets]:
            new_archives.append(archive)
    
    print(f"Found {len(new_archives)} new archives.")
    print(f"New archives: {[a['name'] for a in new_archives]}")
    return new_archives

@task
def download_and_unpack(archive: str, dst_dir: Path):
    archive_id = archive['id']
    
    tar_file = download_tar_file(archive_id)
    ds_name = archive['name']
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    with tarfile.open(fileobj=tar_file, mode="r:*") as tf:
        tf.extractall(dst_dir)
        
    print(f"Unpacked {ds_name} to {dst_dir}")

@task
def collate_dataset(ds_dir: Path):
    merge_subfolders(ds_dir)

@flow(log_prints=True)
def get_raw_datasets():
    archives = []
    drive_archives = []
    
    existing_archives = [
        {
            'name': os.path.splitext(path.split('\\')[-1])[0]
        } for path in os.listdir(RAW_FOLDER)]
    
    if not SERVICE_ACCOUNT_FILE.exists():
        print("No credentials are provided. Checking for new archives only.")
    else:
        drive_archives = get_new_archives()
        if not drive_archives:
            print("No new archives found.")
            return

        for a in drive_archives:
            a['name'] = a['name'].split(".")[0]
            dataset_dir = RAW_FOLDER / a['name']
            
            download_and_unpack(a, dataset_dir)
            
            collate_dataset(dataset_dir)
            print(f"Unpacked {a['name']} to {RAW_FOLDER / a['name']}")
            
        archives = drive_archives
        
    for archive in existing_archives:
        archive_name = archive['name']
        if archive_name not in [a['name'] for a in drive_archives]:
            archives.append(archive)
                
    return archives

if __name__ == "__main__":
    get_raw_datasets()