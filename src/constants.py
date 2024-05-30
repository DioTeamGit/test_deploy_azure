import os
from pathlib import Path


PROJECT_PATH = Path(os.path.dirname(__file__)).parent
DATA_PATH = PROJECT_PATH / "data"
CONTAINER_NAME = "hello-world-cont"
BLOB_NAME = "iris.csv"
