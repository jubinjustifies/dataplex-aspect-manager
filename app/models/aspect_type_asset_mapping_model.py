from pydantic import BaseModel
from typing import List

class AspectType(BaseModel):
    aspect_type_id: str
    gcp_assets: List[str]

class AspectTypeAssetMapping(BaseModel):
    aspect_types: List[AspectType]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)