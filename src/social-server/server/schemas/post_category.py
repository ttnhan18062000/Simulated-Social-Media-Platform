from pydantic import BaseModel


class PostCategoryCreate(BaseModel):
    post_id: int
    category_id: int


class PostCategoryRead(BaseModel):
    post_id: int
    category_id: int

    class Config:
        from_attributes = True
