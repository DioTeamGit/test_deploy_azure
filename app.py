from flask import Flask

from src.make_bucket import push_to_container, read_blob_from_azure_to_dataframe
from src.plotting import import_and_save_iris, plot_iris_dataset_gui

app = Flask(__name__)


def save_iris_and_upload():
    _ = import_and_save_iris()
    push_to_container(path="./data/iris.csv")


@app.route('/')
def hello_world():
    _ = save_iris_and_upload()
    df = read_blob_from_azure_to_dataframe()
    rend = plot_iris_dataset_gui(df)
    return rend


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
