import pandas as pd

def data_cleaning(storage_url:str, container_name:str, data_level:str, filename:str):

    """
    This will return the raw data cleaned into a list of dictionaries

    args:
     - storage_url: This is the connection URL for the storage account
     - container_name: The name of the project's container inside our storage account
     - data_level: Level of data quality -> raw or access
     - filename: Name of the csv file
    """
    
    # Converting the csv containing raw data into a DF
    df = pd.read_csv(f'{storage_url}{container_name}/{data_level}/{filename}')

    # The column "colorsNumber" has this syntax e.g. "2 colors" or "1 Color". Here we are only keeping
    # the numbers
    df["colorsNumber"] = df["colorsNumber"].str.replace(" colors","")
    df["colorsNumber"] = df["colorsNumber"].str.replace(" Color","")

    # These 3 columns are part of the PRIMARY KEY, so they can't be empty
    df["modelName"].replace("","N/A",inplace=True)
    df["lensColor"].replace("","N/A",inplace=True)
    df["localizedColorLabel"].replace("","N/A",inplace=True)

    # There are 2 columns for the product name. Here we are dropping the one with the name "name"
    df.drop(['name'], axis=1, inplace=True)

    # Every column name must be in lowercase
    df.columns = df.columns.str.lower()

    return df.to_dict("records")