from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

DRIVE_RAW_FOLDER_ID = os.environ.get("DRIVE_RAW_FOLDER_ID", "")
DRIVE_PROCESSED_FOLDER_ID = os.environ.get("DRIVE_PROCESSED_FOLDER_ID", "")

if not DRIVE_RAW_FOLDER_ID or not DRIVE_PROCESSED_FOLDER_ID:
    raise ValueError("Please set the environment variables DRIVE_RAW_FOLDER_ID and DRIVE_PROCESSED_FOLDER_ID.")

ROOT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = ROOT_FOLDER / "src" / "data"

RAW_FOLDER = DATA_FOLDER / "raw"
PROCESSED_FOLDER = DATA_FOLDER / "processed"

DATA_SCALING_FACTOR = 0.25

SERVICE_ACCOUNT_FILE = Path(os.path.join(os.path.dirname(__file__), 'credentials', 'credentials.json')).resolve()
SCOPES = ['https://www.googleapis.com/auth/drive']