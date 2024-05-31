import os
import logging

from dotenv import find_dotenv, load_dotenv
from src.make_bucket import list_all_blobs
from src.constants import BLOB_NAME

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
_ = load_dotenv(find_dotenv())


def test_az_key_in_env():
    az_key = os.environ.get("AZ_ACCESS_KEY", "not found")
    assert az_key != "not found"
    assert az_key is not None
    assert len(az_key) != 0


def test_blob_in_bucket():
    try:
        assert BLOB_NAME in list_all_blobs()

    except AssertionError as e:
        logging.info(os.environ.get("AZ_ACCESS_KEY", "not found"))
        raise e
