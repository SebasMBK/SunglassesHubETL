from csv import DictReader
from tabnanny import check
import pandas as pd
import os
from pydantic import ValidationError
from model_pydantic import products

def get_files_names(path) -> list[str]:

    """
    This function returns a list of the files' names that exist in the directory
    """

    files =[]
    for file in os.listdir(path):
        if file.endswith(".csv"):
            files.append(os.path.join(path, file))

    if len(files) == 0:
        print(f"There are no .csv files in {path}")

    return files


def csv_reader(filename:str) -> list[dict]:

    """
    This will return a list of dictionaries containing data from each column of the file

    args:
     - filename: Specify the path of the file.
    """

    try:

        with open(filename, "r",encoding='utf-8-sig') as file:
            get_dictionary = DictReader(file)
            csv_to_list = list(get_dictionary)
        
        return csv_to_list

    except OSError as exception:
        print(f"{filename} - {exception}")


def data_cleaning(raw_data:list) -> list[dict]:

    """
    This will return the raw data cleaned into a list of dictionaries

    args:
     - raw_data: This is a list of dictionaries of the raw data that is required to be cleaned
    """
    
    # Converting the list of dictionaries into a DF.
    df = pd.DataFrame(raw_data)

    # The column "colorsNumber" has this syntax e.g. "2 colors" or "1 Color". Here we are only keeping
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

    return df.to_dict("records")


def convert_to_csv(clean_data: dict, data_level: str, gender: str) -> pd.DataFrame:

    """
    This will write the clean data into a csv file

    args:
     - cleaned_data: List of dictionaries of cleaned data, ready to be written into a csv file
     - data_level: The level of the data -> for example: raw, validated, access, etc.
     - gender: Which file are we working on. Sunglasseshub for men or women
     """
    
    # Converting the list of dictionaries into a DF.
    df = pd.DataFrame(clean_data)
    df.to_csv(f"/tmp/files/access/products-{gender}-{data_level}.csv",encoding="utf-8-sig",sep=';',index=False)

    return df




if __name__ == "__main__":
    files = get_files_names(path="/tmp/files/raw/")
    for file in files:
        gender_file = file.split("-")[1]
        csv_to_list = csv_reader(filename=file)
        access_level_data = data_cleaning(raw_data=csv_to_list)

        # This will do the validations against the pydantic model        
        try:
            validated_file = [products.parse_obj(data_) for data_ in access_level_data]
            write_to_csv = convert_to_csv(clean_data=access_level_data,data_level="access",gender=gender_file)
        except ValidationError as exception:
            print(f"Sunglasses for {gender_file}: {exception}")