from typing import Type, TypeVar, List
from pydantic import TypeAdapter, BaseModel

T = TypeVar("T", bound=BaseModel)

def validate_list(model: Type[T], data: list) -> List[T]:
    """Validates a list of dictionaries against any Pydantic model."""
    adapter = TypeAdapter(List[model])
    return adapter.validate_python(data)
