import logging

from flask import Flask, jsonify

from src.make_bucket import push_to_container, read_blob_from_azure_to_dataframe
from src.plotting import import_and_save_iris, plot_iris_dataset_gui

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Add this to your Flask app
app.logger.setLevel(logging.DEBUG)


def save_iris_and_upload():
    _ = import_and_save_iris()
    push_to_container(path="./data/iris.csv")


@app.route('/')
def hello_world():
    _ = save_iris_and_upload()
    df = read_blob_from_azure_to_dataframe()
    rend = plot_iris_dataset_gui(df)
    return rend


@app.errorhandler(500)
def internal_error(error):
    return jsonify(error=str(error)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
