import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def list_tar_files(folder_id):
    """
    Возвращает список файлов с расширением .tar в заданной папке Google Drive
    :param folder_id: ID папки на Google Drive
    :return: список dict с ключами 'id' и 'name'
    """
    service = get_drive_service()
    query = f"'{folder_id}' in parents and name contains '.tar'"
    results = []
    page_token = None
    while True:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        results.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return results

def download_tar_file(file_id):
    """
    Скачивает файл с заданным file_id и возвращает его содержимое в виде объекта BytesIO.
    :param file_id: ID файла на Google Drive
    :return: BytesIO объект с данными загруженного файла
    """
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download {int(status.progress() * 100)}%.")
    fh.seek(0)
    print(f"File {file_id} downloading is complete.")
    return fh

def upload_tar_file(file_path, folder_id):
    """
    Загружает файл на Google Drive в заданную папку.
    :param file_path: Путь к файлу на локальной машине
    :param folder_id: ID папки на Google Drive
    """
    service = get_drive_service()
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    with open(file_path, "rb") as f:
        media = MediaIoBaseUpload(f, mimetype="application/x-tar", resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"File {file_name} uploaded successfully to folder {folder_id}.")