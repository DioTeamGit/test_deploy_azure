from src.make_bucket import read_blob_from_azure_to_dataframe
from src.plotting import plot_iris_dataset


if __name__ == "__main__":
    df = read_blob_from_azure_to_dataframe()
    plot_iris_dataset(df)