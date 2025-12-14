from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ProductSchema(BaseModel): 
    '''Define como um novo produto ao ser inserido deve ser representado
    '''
    name: str = "Calça"
    description: str = "Calça jeans slim"
    category: str = "men's clothing"
    image_url: str = "https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_t.png"
    price: float = 64.00

class ProductViewSchema(BaseModel):

    name: str
    description: str
    category: str
    image_url: str
    price: float


class ProductListResponse(BaseModel):
    items: list[ProductViewSchema]


class ProductDeleteRequest(BaseModel):
    id: UUID

class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    category: str
    image_url: str
    price: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ProductDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }

