import pathlib
from dotenv import dotenv_values

def config_values():
    script_path = pathlib.Path(__file__).parent.resolve()
    config = dotenv_values(f"{script_path}/configuration.env")
    return config