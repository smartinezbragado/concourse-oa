from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    """
    Model representing a query request with user query and router type.

    Attributes:
        user_query (str): The query provided by the user.
        router_type (str): The type of router to be used for processing the query.
    """
    user_query: str = Field(..., description="The query provided by the user.")
    router_type: str = Field(..., description="The type of router to be used for processing the query.")

    @field_validator('router_type')
    def validate_router_type(cls, value):
        allowed_types = {'semantic', 'llm'}
        if value not in allowed_types:
            raise ValueError(f"router_type must be one of {allowed_types}")
        return value
