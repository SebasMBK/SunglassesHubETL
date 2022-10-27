from pydantic import BaseModel

# In this file, lies the code for the data validation to ensure the righ quality before the ingestion
# and after the data cleaning.

class products(BaseModel):
    """
    Pydantic model to validate the schema of the extracted files.
    All files extracted should have the same schema, so we only need 1 class.
    """

    

