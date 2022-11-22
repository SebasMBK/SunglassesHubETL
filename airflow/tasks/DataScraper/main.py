from scraper_men_products import scraper_men
from scraper_women_products import scraper_women
import pathlib
from dotenv import dotenv_values 

if __name__ == "__main__":

    script_path = pathlib.Path(__file__).parent.parent.resolve()
    config = dotenv_values(f"{script_path}/configuration.env")
    data_level = config["raw_data_directory"]

    scraper_men(data_level=data_level)
    scraper_women(data_level=data_level)



    


