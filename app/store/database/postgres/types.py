from typing import TypeVar, Union

from sqlalchemy import UpdateBase, ValuesBase
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from sqlalchemy.sql import Delete, Insert, Select

Query = Union[ValuesBase, Select, UpdateBase, Delete, Insert]
Model = TypeVar("Model", bound=DeclarativeAttributeIntercept)
