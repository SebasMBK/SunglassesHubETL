from csv import DictReader
import pandas as pd
import os

files = []
files_path = "./files/raw/"

for file in os.listdir("./files/raw/"):
    if file.endswith(".csv"):
        files.append(os.path.join("./files/raw/", file))


def csv_reader(filename:str) -> list[dict]:
    
    """
    This will return a list of dictionaries containing data from each column of the file

    args:
     - filename: Specify the path of the file.
    """

    with open(filename, "r",encoding='utf-8-sig') as file:
        get_dictionary = DictReader(file)
        csv_to_list = list(get_dictionary)
        return dict_to_csv


def data_cleaning(raw_data:list):
    """
    This will return the raw data cleaned and converted into a pandas DataFrame

    args:
     - raw_data: This is a list of dictionaries of the raw data that is required to be cleaned
    """

    df = pd.DataFrame(raw_data)
    df["listPrice"] = df["listPrice"].str.replace("$","")
    df["offerPrice"] = df["offerPrice"].str.replace("$","")

    #diccionario = arch.to_dict("records")
    #print(diccionario[2])
