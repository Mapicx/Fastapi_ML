from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional


class PredictInput(BaseModel):
    Clump_Thickness: int
    Uniformity_of_Cell_Size: int
    Uniformity_of_Cell_Shape: int
    Marginal_Adhesion: int
    Single_Epithelial_Cell_Size: int
    Bare_Nuclei: int
    Bland_Chromatin: int
    Normal_Nucleoli: int
    Mitoses: int
    

class PredictResponse(BaseModel):
    id: int
    result : int




class Token(BaseModel):
    access_token : str
    token_type : str

class Token_data(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]