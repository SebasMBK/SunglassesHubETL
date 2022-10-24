from csv import DictReader
import pandas as pd

files = ["./archivos/products-men-raw.csv","./archivos/products-women-raw.csv"]


def csv_reader(filename:str) -> list[dict]:
    
    """
    This will return a list of dictionaries containing data from each column of the file

    args:
     - filename: Specify the path of the file.
    """

    with open(filename, "r",encoding='utf-8-sig') as file:
        get_dictionary = DictReader(file)
        list_csv = list(get_dictionary)
    
    return list_csv
    
#men = csv_reader(files[0])
men = pd.DataFrame(csv_reader(files[0]))
#women = pd.DataFrame(csv_reader(files[1]))
#print(float((men[0]["listPrice"]).replace("$","")))
men["listPrice"] = men["listPrice"].str.replace("$","")
men["offerPrice"] = men["offerPrice"].str.replace("$","")
diccionario = men.to_dict("records")
print(diccionario[0])
