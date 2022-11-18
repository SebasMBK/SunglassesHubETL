from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import pandas as pd
from dotenv import dotenv_values
import pathlib

def azure_upload_df(dataframe=None, filename=None, datalevel=None):
    """
    Upload DataFrame to Azure Blob Storage for given container
    Keyword arguments:
    dataframe -- the dataframe(df) object (default None)
    filename -- the filename to use for the blob (default None)
    datalevel -- raw or access

    """
    script_path = pathlib.Path(__file__).parent.resolve()
    config = dotenv_values(f"{script_path}/configuration.env")
    # get environment values:

    storage_account_url = config["storage_account_url"]
    container = config["etl_container_name"]


    azure_credentials = DefaultAzureCredential()
    if all([container, len(dataframe), filename]):
        upload_file_path = rf"{datalevel}\{filename}"
        blob_service_client = BlobServiceClient(f"{storage_account_url}",credential=azure_credentials)
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=upload_file_path
        )

        try:
            output = dataframe.to_csv(index=False, encoding="utf-8")
        except Exception as e:
            print(e)

        try:
            blob_client.upload_blob(output, blob_type="BlockBlob",overwrite=True)
        except Exception as e:
            print(e)