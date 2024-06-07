# from src.make_bucket import read_blob_from_azure_to_dataframe
# from src.plotting import plot_iris_dataset

from azure.storage.blob import BlobServiceClient
import os


if __name__ == "__main__":
    # df = read_blob_from_azure_to_dataframe()
    # plot_iris_dataset(df)
    conn_string=os.environ.get("AZ_ACCESS_KEY")
    print(conn_string)
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        print("All Good")

    except Exception as e:
        raise e
    

        