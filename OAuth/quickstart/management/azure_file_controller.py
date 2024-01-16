from io import BytesIO
import uuid
from pathlib import Path

from azure.storage.blob import BlobClient
from django.conf import settings
from azure.storage.blob import BlobServiceClient
service = BlobServiceClient(account_url="https://testfyp.blob.core.windows.net/test", credential="M/7QSQ3Y2bYem5E+BvzQoAymK42l4VMiOa0ZkJh7l+b65I9wZrMb7tocD1ty+aHhsF3WNXBRRh8Q+ASt8WldBQ==")


def download_blob(file):
    blob_client = service.get_blob_client(container="test",blob=file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content
    

def upload_file_to_blob(file):

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    blob_client = service.get_blob_client(container="test",blob=file_name)
    blob_client.upload_blob(data=file_io)

    return blob_client.url