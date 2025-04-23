from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

RAW_FOLDER_ID = os.environ.get("RAW_FOLDER_ID", "raw_data")
PROCESSED_FOLDER_ID = os.environ.get("PROCESSED_FOLDER_ID", "processed_data")

ROOT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = ROOT_FOLDER / "data"

DATA_SCALING_FACTOR = 0.25