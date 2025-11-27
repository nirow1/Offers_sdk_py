from pydantic import BaseModel, Field
from uuid import UUID

class RegisterProductSchema(BaseModel):
    id: UUID = Field(..., description="Product ID")
    name: str = Field(..., min_length=1, description="Product name cannot be empty")
    description: str = Field(..., min_length=1, description="Product description cannot be empty")
