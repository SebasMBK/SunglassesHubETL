from locale import currency
from pydantic import BaseModel, validator

# In this file, lies the code for the data validation to ensure the righ quality before the ingestion
# and after the data cleaning.

class products(BaseModel):
    """
    Pydantic model to validate the schema of the extracted files.
    All files extracted should have the same schema, so we only need 1 class.
    """
    isjunior: bool
    lenscolor: str
    img: str
    isfindinstore: bool
    iscustomizable: bool
    roxablelabel: str
    brand: str
    imghover: str
    ispolarized: bool
    colorsnumber: int
    isoutofstock: bool
    modelname: str
    isengravable: bool
    localizedcolorlabel: str
    # Both prices contains "$" signs. Therefore they are considered as strings by python
    listprice: str
    offerprice: str

    @validator('modelname')
    def not_null_modelname(cls,modelname):
        if modelname == '':
            raise ValueError("modelname can't be null")
        return modelname
    
    @validator('lenscolor')
    def not_null_lenscolor(cls,lenscolor):
        if lenscolor == '':
            raise ValueError("lenscolor can't be null")
        return lenscolor
    
    @validator('localizedcolorlabel')
    def not_null_localizedcolorlabel(cls,localizedcolorlabel):
        if localizedcolorlabel == '':
            raise ValueError("localizedcolorlabel can't be null")
        return localizedcolorlabel




    

