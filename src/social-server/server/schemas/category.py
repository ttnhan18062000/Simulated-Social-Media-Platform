from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryRead(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
