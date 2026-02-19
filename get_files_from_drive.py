from googleapiclient.discovery import build


def get_files_from_drive(creds, folder_id):
    drive_service = build('drive', 'v3', credentials=creds)
    files = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed = false").execute().get('files', [])
    return files
