from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.schemas.product_schemas import ProductResponse
from app.schemas.stock_schemas import StockResponse, StockViewSchema


class ConditionalItemSchema(BaseModel):
    '''Define como um novo produto ao ser inserido deve ser representado
    '''
    conditional_id: UUID
    product_stock_id: UUID
    quantity: int
    final_action: str | None
    

class ConditionalItemViewSchema(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após o GET'''

    id: UUID
    conditional_id: UUID
    product_stock_id: UUID
    quantity: int
    returned_quantity: int | None
    purchased_quantity: int | None
    final_action: str | None
    updated_at: datetime | None
    product: ProductResponse | None
    product_stock: StockResponse | None

    model_config = {
        "from_attributes": True
    }


class ConditionalItemResponse(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após uma adição'''

    id: UUID
    conditional_id: UUID    
    quantity: int
    returned_quantity: int | None = 0
    purchased_quantity: int | None = 0
    final_action: str | None = None
    product_stock: StockViewSchema
    
    model_config = {
        "from_attributes": True
    }


class ConditionalItemListResponse(BaseModel):
    items: list[ConditionalItemViewSchema]

    model_config = {
        "from_attributes": True
    }


class ConditionalItemPath(BaseModel):
    item_id: UUID


class ConditionalItemDeleteResponse(BaseModel):
    message: str


class ConditionalItemReturn(BaseModel):
    item_id: UUID    
    returned_quantity: int | None    

class ConditionalReturnForm(BaseModel):
    items: List[ConditionalItemReturn]