import os
from data_validation import get_files_names


files = get_files_names()


for file in files:
    file_name = "sunglasseshub_" + file.split("-")[1] + "_table"
    print(file_name)