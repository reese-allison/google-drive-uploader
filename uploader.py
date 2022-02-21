import requests
import tempfile

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    'https://www.googleapis.com/auth/drive.file'
]

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        'service-account.json', scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def create_folder(service, message):
    file_metadata = {
        'name': message.channel.name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(
        body=file_metadata,                                
        fields='id'
    ).execute()
    permission = {
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file.get('id'), body=permission).execute()
    return file.get('id') 

def create_file(service, folder_id, attachment):
    tmp_file = tempfile.NamedTemporaryFile(
        delete=False
    )
    try:
        tmp_file.write(
            requests.get(attachment.url, stream=True).content
        )
        file_metadata = {
            'name': attachment.filename,
            'mimeType': attachment.content_type,
            'parents': [folder_id]
        }
        media = MediaFileUpload(
            tmp_file.name,
            mimetype=attachment.content_type,
            resumable=True
        )
        file = service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        permission = {
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(fileId=file.get('id'), body=permission).execute()
        return file.get('id')
    finally:
        tmp_file.close()


def get_folder(service, message):
    file_name = message.channel.name
    page_token = None
    while True:
        response = service.files().list(
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        for file in response.get('files', []):
            if file_name == file.get('name'):
                return file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return create_folder(service, message)

async def upload(message, attachment):
    service = get_service()
    folder_id = get_folder(service, message)
    file_id = create_file(service, folder_id, attachment)
    with open("sync", "w") as file:
        file.write(str(message.id))
    return create_file_link(file_id)

async def get_drive(message):
    service = get_service()
    folder_id = get_folder(service, message)
    return create_folder_link(folder_id)

def create_file_link(file_id):
    return f'https://drive.google.com/file/d/{file_id}/view'

def create_folder_link(folder_id):
    return f'https://drive.google.com/drive/u/0/folders/{folder_id}'
