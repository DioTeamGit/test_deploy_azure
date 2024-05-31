import base64
from io import BytesIO

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from flask import render_template_string

from .constants import DATA_PATH
from .make_bucket import list_all_blobs


def import_and_save_iris(path: str = DATA_PATH):
    if not "iris.csv" in [
        file.split("/")[-1] for file in os.listdir(path)
    ]:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['species'] = iris.target
        df['species'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
        df.to_csv(DATA_PATH.as_posix() + "/iris.csv")


def plot_iris_dataset_gui(df: pd.DataFrame):
    # Create a pairplot using Seaborn

    _ = plt.Figure()
    sns.set_theme(style="ticks")
    pairplot = sns.pairplot(
        df, 
        hue='species', 
        markers=["o", "s", "D"],
        plot_kws={'alpha': 0.5},
    )
    pairplot.figure.suptitle("Iris Dataset Pairplot", y=1.02)

    # plt.show()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # HTML template with the plot embedded
    html_template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Hello, world!</title>
      </head>
      <body>
        <div class="container">
          <h1>LA PRIMA APP DI P4I SU AZURE SIIIIIII!</h1>
          <h1>Tiè, pijate sto plot:</h1>
          <img src="data:image/png;base64,{{ plot_url }}" alt="Plot">
        </div>
      </body>
    </html>
    """
    return render_template_string(html_template, plot_url=plot_url)

    # return fig
