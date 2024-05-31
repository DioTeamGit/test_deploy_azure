import os

from dotenv import find_dotenv, load_dotenv
from src.make_bucket import list_all_blobs
from src.constants import BLOB_NAME

_ = load_dotenv(find_dotenv())

def test_az_key_in_env():
    az_key = os.environ.get("AZ_ACCESS_KEY", "not found")
    assert az_key != "not found"
    assert az_key is not None


def test_blob_in_bucket():
    try:
        assert BLOB_NAME in list_all_blobs()

    except AssertionError as e:
        print(os.environ.get("AZ_ACCESS_KEY", "not found"))
        raise e
