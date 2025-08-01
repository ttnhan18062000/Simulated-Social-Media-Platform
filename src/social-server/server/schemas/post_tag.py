from pydantic import BaseModel


class PostTagCreate(BaseModel):
    post_id: int
    tag_id: int


class PostTagRead(BaseModel):
    post_id: int
    tag_id: int

    class Config:
        from_attributes = True
