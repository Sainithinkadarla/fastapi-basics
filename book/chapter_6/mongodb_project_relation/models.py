from bson import ObjectId
from datetime import datetime
from typing import Any

from pydantic import Field, BaseModel, ConfigDict
from pydantic_core import core_schema, PydanticCustomError
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def validate_object_id(cls, value: Any) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str):
            if not ObjectId.is_valid(value):
                raise PydanticCustomError('InvalidObjectId', 'Invalid ObjectId')
            return ObjectId(value)
        raise PydanticCustomError('InvalidObjectId', 'Invalid ObjectId')

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_before_validator_function(
            cls.validate_object_id,
            core_schema.is_instance_schema(ObjectId)
        )
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="ObjectId")
        return json_schema

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True, 
        arbitrary_types_allowed=True,
        json_encoders = {ObjectId: str}
    )

class CommentBase(BaseModel):
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    pass

class PostBase(MongoBaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

class Post(PostBase):
    comments: list[Comment] = Field(default_factory=list)

class PostCreate(PostBase):
    pass

class PostPartialUpdate(BaseModel):
    title : str | None = None
    content : str | None = None