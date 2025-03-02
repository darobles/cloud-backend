from pydantic import BaseModel
from typing import Optional, List, Union

class ProductStock(BaseModel):
    # Define fields for product stock if needed
    ...

class Brand(BaseModel):
    # Define the fields for Brand if needed
    ...

class CustomFields(BaseModel):
    # Define your custom fields
    ...

class ProductType(BaseModel):
    # You can later convert this to an Enum if there are fixed values (e.g. "type: Literal[...]")
    ...

class PartReturn(BaseModel):
    id: int
    excerpt: str
    slug: str
    sku: Optional[str] = None
    partNumber: str
    stock: ProductStock
    compareAtPrice: Optional[float] = None
    images: Optional[List[str]] = None
    badges: Optional[List[str]] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    availability: Optional[str] = None
    alert: Optional[str] = None
    barcode: str
    committedlevel: int
    description: Optional[str] = None    
    make_dbid: str
    model_dbid: str
    model_id: int
    brand: Optional[Brand] = None
    name: str
    othermodel: Optional[str] = None
    part_dbid: str
    part_new: bool
    part_old: bool
    part_perf: bool
    part_stocklevel: int
    picture: int
    price: float
    price1: str
    price2: str
    price3: str
    price4: str
    price5: str
    price6: str
    showmemberonly: bool
    special: bool
    submodel: Optional[str] = None
    updated: str
    tags: Optional[List[str]] = None
    type: ProductType
    categories: Optional[List] = None
    attributes: List = []
    compatibility: Union[str, List[int]]
    options: List = []
    customFields: Optional[CustomFields] = None