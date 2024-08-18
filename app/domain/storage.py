from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account

from app import config


class StorageBase(ABC):

    @abstractmethod
    def upload_file(
        self, bucket_name: str, source_file_path: str, destination_blob_name: str
    ):
        """Uploads a file to an object storage bucket.

        Args:
            bucket_name: Name of the bucket.
            source_file_path: Path to the local file.
            destination_blob_name: Name of the object in the bucket.
        """
        ...

    @abstractmethod
    def upload_bytes(
        self, bucket_name: str, data: bytes, destination_blob_name: str
    ) -> None:
        """Uploads bytes to an objct storage bucket.

        Args:
            bucket_name: Name of the bucket.
            data: Bytes to upload.
            destination_blob_name: Name of the object in the bucket.
        """
        ...

    @abstractmethod
    def generate_download_urls(self, bucket_name: str, prefix: str, expiration: int):
        """Generates signed URLs for objects in an object storage bucket.

        Args:
            bucket_name: Name of the bucket.
            prefix: Prefix to filter objects (e.g., 'images/').
            expiration: Expiration time for the generated URLs.
        Returns:
            A list of signed URLs.
        """
        ...

    @abstractmethod
    def generate_download_url(
        self, bucket_name: str, blob_name: str, expiration: int
    ) -> str:
        """Generates a signed URL for a single object in an object storage bucket.

        Args:
            bucket_name: Name of the bucket.
            blob_name: Name of the object.
            expiration: Expiration time for the generated URL.

        Returns:
            The generated signed URL.
        """
        ...


class GCPStorage(StorageBase):
    """A class for interacting with Google Cloud Storage."""

    def __init__(self, key_file_path: Optional[str] = None) -> None:
        """Initializes the GCPStorage object.

        Args:
            key_file_path: Path to the service account key file. If not provided,
                Application Default Credentials will be used.
        """

        if not key_file_path:
            key_file_path = config.GCP_AUTH_SERVICE_FILE

        if key_file_path:
            self.credentials = service_account.Credentials.from_service_account_file(
                key_file_path
            )
        else:
            # Use Application Default Credentials
            self.credentials = None
        self.client = storage.Client(credentials=self.credentials)

    def upload_file(
        self, bucket_name: str, source_file_path: str, destination_blob_name: str
    ) -> None:
        """Uploads a file to a Google Cloud Storage bucket.

        Args:
            bucket_name: Name of the bucket.
            source_file_path: Path to the local file.
            destination_blob_name: Name of the object in the bucket.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)

    def upload_bytes(
        self, bucket_name: str, data: bytes, destination_blob_name: str
    ) -> None:
        """Uploads bytes to a Google Cloud Storage bucket.

        Args:
            bucket_name: Name of the bucket.
            data: Bytes to upload.
            destination_blob_name: Name of the object in the bucket.
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(data)
        except GoogleCloudError as e:
            raise e

    def generate_download_urls(
        self, bucket_name: str, prefix: str, expiration: int = 604800
    ) -> List[str]:
        """Generates signed URLs for objects in a Google Cloud Storage bucket.

        Args:
            bucket_name: Name of the bucket.
            prefix: Prefix to filter objects (e.g., 'images/').
            expiration: Expiration time for the generated URLs in seconds. Defaults to 7 days.

        Returns:
            A list of signed URLs.
        """
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        signed_urls = []
        for blob in blobs:
            url = blob.generate_signed_url(expiration=expiration, method="GET")
            signed_urls.append(url)

        return signed_urls

    def generate_download_url(
        self, bucket_name: str, blob_name: str, expiration: int = 604800
    ) -> str:
        """Generates a signed URL for a single object in a Google Cloud Storage bucket.

        Args:
            bucket_name: Name of the bucket.
            blob_name: Name of the object.
            expiration: Expiration time for the generated URL in seconds. Defaults to 7 days.

        Returns:
            The generated signed URL.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        url = blob.generate_signed_url(expiration=expiration, method="GET")
        return url
