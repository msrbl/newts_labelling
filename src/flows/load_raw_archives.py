from pathlib import Path
from prefect import flow, task
from src.data_io.drive.drive_manager import list_tar_files, download_tar_file
import tarfile
import shutil
import subprocess
import os
import re

from src.config import DATA_FOLDER, RAW_FOLDER_ID
import json
import io

from src.flows.aggregate_data import end_to_end_dataset

@task
def get_new_archives() -> list[dict]:
    raw_archives = list_tar_files(RAW_FOLDER_ID)
    with open(DATA_FOLDER / "processed_datasets.json", "r") as f:
        processed = json.load(f)
    processed_names = {}
    if processed:
        processed_names = {item['name'] for item in processed}

    pattern = r"^(?P<name>[^/]+)\.tar$"
    new_archives = []
    for archive in raw_archives:
        match = re.match(pattern, archive['name'])
        if match:
            archive_name = match.group("name")
            if archive_name not in processed_names:
                new_archives.append(archive)
    print(f"Found {len(new_archives)} new archives.")
    print(f"New archives: {[a['name'] for a in new_archives]}")
    return new_archives

@task
def download_and_unpack(archive: str, raw_folder: Path) -> str:
    archive_id = archive['id']
    
    tar_file = download_tar_file(archive_id)
    ds_name = archive['name']
    dst_dir = raw_folder / ds_name
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    with tarfile.open(fileobj=tar_file, mode="r:*") as tf:
        tf.extractall(dst_dir)
    return ds_name

@flow(log_prints=True)
def load_raw_dataset(raw_folder: Path):
    archives = get_new_archives()
    if not archives:
        print("No new archives found.")
        return
    
    for a in archives:
        a['name'] = a['name'].split(".")[0]
        
        # download_and_unpack(a, raw_folder)
        print(f"Unpacked {a['name']} to {raw_folder / a['name']}")
        
    return archives