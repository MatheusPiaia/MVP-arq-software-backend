from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CustomerSchema(BaseModel):
    '''Define como um cliente ao ser adicionado a base
    deve ser representado'''

    name: str = "Maria"
    phone: str = "(49) 999999999"
    address: str = "Avenida do lago 122"


class CustomerViewSchema(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após o GET'''

    id:UUID    
    name: str
    phone: str
    address: str    

    model_config = {
        "from_attributes": True
    }


class CustomerResponse(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após uma adição'''

    id: UUID
    name: str
    phone: str
    address: str

    model_config = {
        "from_attributes": True
    }


class CustomerListResponse(BaseModel):
    items: list[CustomerViewSchema]