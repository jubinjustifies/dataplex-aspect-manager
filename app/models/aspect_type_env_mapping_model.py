from pydantic import BaseModel
from typing import List

class AspectTypeEnv(BaseModel):
    aspect_type_id: str
    gcp_project_id: str
    location_id: str

class AspectTypeEnvMapping(BaseModel):
    aspect_types: List[AspectTypeEnv]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)