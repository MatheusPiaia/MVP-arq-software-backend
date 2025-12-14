from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.schemas.conditional_items_schemas import ConditionalItemListResponse, ConditionalItemResponse
from app.schemas.customer_schemas import CustomerViewSchema


class ConditionalSchema(BaseModel):
    '''Define como um condicional ao ser adicionado a base
    deve ser representado
    '''

    customer_id: UUID = "0c9dced1-88b6-43bf-99d3-7c42c61c4c57"
    user_id: UUID = "543c73ca-2f9c-420f-a789-6ab770ef0f39"
    status: str = "open"


class ConditionalViewSchema(BaseModel):
    '''Define como deve ser a estrutura do dado retornado
    após o GET'''

    id: UUID
    user_id: UUID
    status: str
    created_at: datetime | None
    closed_at: datetime | None
    customer: CustomerViewSchema
    items: list[ConditionalItemResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


class ConditionalListResponse(BaseModel):
    items: list[ConditionalViewSchema]


class ConditionalPath(BaseModel):
    conditional_id: UUID


class ConditionalStatusResponse(BaseModel):
    status: str

