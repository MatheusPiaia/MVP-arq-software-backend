from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.schemas.product_schemas import ProductResponse


class StockSchema(BaseModel):
    '''Define como um produto ao ser adicionado
    no estoque deve ser representado'''

    product_id:UUID
    size:str = "P"
    color:str = "Red"
    quantity:int = 2


class StockUpdateSchema(BaseModel):
    '''Define como deve ser a estrutura do dado
    para editar estoque de um produto'''
    quantity_available: Optional[int] = None
    quantity_reserved: Optional[int] = None


class StockViewSchema(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após o GET'''

    id:UUID    
    size: str
    color: str
    quantity_available: int
    quantity_reserved: int
    quantity_real: int
    updated_at: datetime | None
    product: ProductResponse

    model_config = {
        "from_attributes": True
    }


class StockResponse(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após uma adição'''

    id:UUID    
    size: str
    color: str
    quantity_available: int
    quantity_reserved: int
    quantity_real: int       

    model_config = {
        "from_attributes": True
    }


class StockListResponse(BaseModel):
    items: list[StockViewSchema]


class StockPath(BaseModel):
    stock_id: UUID


class StockFilterQuery(BaseModel):
    size: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    reference: Optional[str] = None