"""
GraphQL definitions file.
"""
import re
from dataclasses import dataclass
from typing import List, Optional

from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow.schema import Schema


class GraphObject:
    """
    A class wrapper for the GraphQL query.
    This class can be further wrapped with other GraphObject classes that
    add more functionality to the original query.
    """

    def __init__(self, object_name, query, resp_schema, query_variables):
        self.object_name = object_name
        self.query = query
        self.resp_schema = resp_schema
        self.query_variables = query_variables


class GraphqlParsingError(Exception):
    """
    An error that's returned when a problem occurs parsing the Graphql response
    """

    def __init__(self, message):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class SchemaBase(Schema):
    dataclass = None
    snake_case_regex1 = re.compile("(.)([A-Z][a-z]+)")
    snake_case_regex2 = re.compile("([a-z0-9])([A-Z])")

    def __init__(self, *args, **kwargs):
        super(SchemaBase, self).__init__(*args, **kwargs)

    def camel_to_snake(self, name):
        name = self.snake_case_regex1.sub(r"\1_\2", name)
        return self.snake_case_regex2.sub(r"\1_\2", name).lower()

    @post_load
    def to_object(self, data: dict, *_args, **_kwargs):
        """This method turns the schema into its corresponding object."""
        if self.dataclass is None:
            raise ValueError(f"dataclass must be set for {type(self)}")
        if not isinstance(data, dict):
            raise ValueError("data must be of type dict")
        normalized_data = {
            self.camel_to_snake(key): value for key, value in data.items()
        }

        return self.dataclass(**normalized_data)


class NodesSchema(SchemaBase):
    def __iter__(self):
        yield from self.nodes


@dataclass
class Location:
    """
    This class holds the location part of the error.
    """

    line: int
    column: int


@dataclass
class Extension:
    """
    This class holds the extensions part of the error.
    """

    code: Optional[str] = None


@dataclass
class GraphqlError(Exception):
    """
    This class holds a GraphQL error.
    """

    message: str
    locations: Optional[List[Location]] = None
    path: Optional[List[str]] = None
    extensions: Optional[Extension] = None

    def __str__(self):
        return f"{self.extensions.code}: {self.message} ({self.locations[0]}), path {self.path}"


class LocationSchema(SchemaBase):
    """
    Schema for GraphQL location part of the error.
    """

    dataclass = Location

    line = fields.Int(required=True)
    column = fields.Int(required=True)


class ExtensionsSchema(SchemaBase):
    """
    Schema for GraphQL extensions part of the error.
    """

    dataclass = Extension
    code = fields.Str()


class GraphqlErrorSchema(Schema):
    """
    Schema for GraphQL error.
    """

    message = fields.Str(required=True)
    path = fields.List(fields.Str())
    locations = fields.List(fields.Nested(LocationSchema), allow_none=True)
    extensions = fields.Nested(ExtensionsSchema, allow_none=True)

    @post_load
    def to_object(self, data, **_kwargs):
        """This method turns the schema into its corresponding object."""
        return GraphqlError(**data)
