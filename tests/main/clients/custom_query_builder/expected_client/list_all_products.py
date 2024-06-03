from typing import List, Optional

from .base_model import BaseModel


class ListAllProducts(BaseModel):
    products: Optional["ListAllProductsProducts"]


class ListAllProductsProducts(BaseModel):
    edges: List["ListAllProductsProductsEdges"]


class ListAllProductsProductsEdges(BaseModel):
    node: "ListAllProductsProductsEdgesNode"


class ListAllProductsProductsEdgesNode(BaseModel):
    id: str
    slug: str


ListAllProducts.model_rebuild()
ListAllProductsProducts.model_rebuild()
ListAllProductsProductsEdges.model_rebuild()
