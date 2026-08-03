from typing import List
from pydantic import BaseModel


class Dataset(BaseModel):
    name : str #bank marketing
    items : List[str] #name, age, job, ...
