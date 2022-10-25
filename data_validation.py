from csv import DictReader
from tabnanny import check
import pandas as pd
import os

def get_files_names(path) -> list[str]:

    """
    This function returns a list of the files' names that exist in the directory
    """
    files =[]
    for file in os.listdir(path):
        if file.endswith(".csv"):
            files.append(os.path.join(path, file))
    return files


def csv_reader(filename:str) -> list[dict]:
    
    """
    This will return a list of dictionaries containing data from each column of the file

    args:
     - filename: Specify the path of the file.
    """

    with open(filename, "r",encoding='utf-8-sig') as file:
        get_dictionary = DictReader(file)
        csv_to_list = list(get_dictionary)
        return csv_to_list


def data_cleaning(raw_data:list, data_level: str, gender: str) -> pd.DataFrame:
    """
    This will return the raw data cleaned and converted into a pandas DataFrame and then write it
    into a csv file.

    args:
     - raw_data: This is a list of dictionaries of the raw data that is required to be cleaned
     - data_level: The level of the data -> for example: raw, validated, access, etc.
     - gender: Which file are we working on. Sunglasseshub for men or women
    """
    
    # Converting the list of dictionaries into a DF.
    df = pd.DataFrame(raw_data)
    # The column "colorsNumber" has this syntax e.g "2 colors" or "1 Color". Here we are keeping only
    # the numbers
    df["colorsNumber"] = df["colorsNumber"].str.replace(" colors","")
    df["colorsNumber"] = df["colorsNumber"].str.replace(" Color","")
    # These 3 columns are part of the PRIMARY KEY, so they can't be null
    df["modelName"].replace("","N/A",inplace=True)
    df["lensColor"].replace("","N/A",inplace=True)
    df["localizedColorLabel"].replace("","N/A",inplace=True)
    # There are 2 columns for the product name. Here we are dropping the one with the name "name"
    df.drop(['name'], axis=1, inplace=True)
    # Every column name must be in lowercase
    df.columns = df.columns.str.lower()
    # Write DF to csv file
    df.to_csv(f"./files/access/products-{gender}-{data_level}.csv",encoding="utf-8-sig",index=False)

    return df


if __name__ == "__main__":
    files = get_files_names(path="./files/raw/")
    for file in files:
        gender_file = file.split("-")[1]
        csv_file = csv_reader(filename=file)
        raw_dict = data_cleaning(raw_data=csv_file,data_level="access",gender=gender_file)
