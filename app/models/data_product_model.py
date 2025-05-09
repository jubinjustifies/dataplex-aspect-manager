from pydantic import BaseModel
from typing import List, Dict, Optional

class Asset(BaseModel):
    asset_name: str
    flag: str
    
class AssetType(BaseModel):
    asset_type_id: str
    assets: List[Asset]

class Location(BaseModel):
    location_id: str
    asset_types: List[AssetType]

class GCPProject(BaseModel):
    project_id: str
    locations: List[Location]

class DataProduct(BaseModel):
    product_id: str
    gcp_projects: List[GCPProject]


