from bson import ObjectId
from datetime import datetime
from typing import Any

from pydantic import Field, BaseModel, ConfigDict
# Import necessary Pydantic v2 components for custom types
from pydantic_core import core_schema, PydanticCustomError
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    """
    Custom type for reading and writing MongoDB ObjectIds using Pydantic v2.
    It defines a custom core schema for validation and a custom JSON schema for OpenAPI.
    """

    # V2-compliant method for validation logic
    @classmethod
    def validate_object_id(cls, value: Any) -> ObjectId:
        # Allow the value to be passed as an ObjectId (from Motor) or a string (from API request)
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
        # Use a `no_info_before_validator` to run `validate_object_id` before pydantic processes the input.
        # It accepts any type (str from API, ObjectId from database) and ensures it's a valid ObjectId.
        return core_schema.no_info_before_validator_function(
            cls.validate_object_id,
            # The final type that Pydantic sees internally is an instance of ObjectId
            core_schema.is_instance_schema(ObjectId)
        )
    
    # V2-compliant method for JSON Schema (OpenAPI) generation
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any) -> JsonSchemaValue:
        # Generate the default schema, then override the type/format to string/ObjectId
        json_schema = handler(core_schema)
        # Apply the correct JSON schema properties
        json_schema.update(type="string", format="ObjectId")
        return json_schema

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Configuration for Pydantic v2 models
    model_config = ConfigDict(
        populate_by_name=True, 
        arbitrary_types_allowed=True,
        # This encoder converts ObjectId to str when serializing to JSON
        json_encoders = {ObjectId: str}
    )

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

class Post(PostBase):
    pass

class PostCreate(PostBase):
    pass

class PostPartialUpdate(BaseModel):
    title : str | None = None
    content : str | None = None