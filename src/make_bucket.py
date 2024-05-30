import os
import logging
from typing import List, Union, Optional
from io import StringIO

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from azure.storage.blob import BlobServiceClient
from .constants import CONTAINER_NAME, BLOB_NAME

_ = load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)


def __check_not_client(
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    client: Optional[BlobServiceClient] = None
) -> BlobServiceClient:

    if not client:
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)

    else:
        blob_service_client = client

    return blob_service_client


def list_all_buckets(
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    client: Optional[BlobServiceClient] = None
) -> List[str]:
 
    blob_service_client = __check_not_client(conn_string=conn_string, client=client)

    return blob_service_client.list_containers()


def list_all_blobs(
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    container_name: str = CONTAINER_NAME,
    client: Optional[BlobServiceClient] = None
) -> List[str]:

    blob_service_client = __check_not_client(conn_string=conn_string, client=client)

    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the container
    blob_list = container_client.list_blobs()
    return [blob.name for blob in blob_list]


def make_bucket(
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    container_name: str = CONTAINER_NAME,
    client: Optional[BlobServiceClient] = None
) -> BlobServiceClient:

    blob_service_client = __check_not_client(conn_string=conn_string, client=client)
    container_client = blob_service_client.get_container_client(container_name)

    if container_client.exists():
        logger.info(
            "The container has been already created."
        )

    else:
        logger.info(
            f"Creating container {container_name} ----> "
        )
        blob_service_client = blob_service_client.create_container(container_name)

    return blob_service_client


def push_to_container(
    path: Union[str, List[str]],
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    container_name: str = CONTAINER_NAME,
    client: Optional[BlobServiceClient] = None
) -> BlobServiceClient:

    blob_service_client = __check_not_client(conn_string=conn_string, client=client)
    blob_service_client = make_bucket(
        conn_string=conn_string, container_name=container_name, client=blob_service_client
    )

    path = [path] if not isinstance(path, list) else path

    for local_file_name in path:
        blob_name = local_file_name.split("/")[-1]
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)

        # Upload the file
        if blob_name in list_all_blobs(
            conn_string=conn_string, container_name=container_name, client=client
        ):
            logger.info(f"{local_file_name} already uploaded.")

        else:
            logger.info(f"Uploading file: {local_file_name}")
            with open(local_file_name, "rb") as data:
                blob_client.upload_blob(data)

    return blob_client


def read_blob_from_azure_to_dataframe(
    conn_string: str = os.environ.get("AZ_ACCESS_KEY"),
    container_name: str = CONTAINER_NAME,
    client: Optional[BlobServiceClient] = None,
    blob_name: str = BLOB_NAME
) -> pd.DataFrame:

    # Initialize BlobServiceClient
    blob_service_client = __check_not_client(conn_string=conn_string, client=client)
    container_client = blob_service_client.get_container_client(container_name)
    # Get the blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Download the blob to a BytesIO object
    blob_data = blob_client.download_blob().content_as_text()
    data_stream = StringIO(blob_data)

    # Read the data into a pandas DataFrame
    df = pd.read_csv(data_stream)
    return df
