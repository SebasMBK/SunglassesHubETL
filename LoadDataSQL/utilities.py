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