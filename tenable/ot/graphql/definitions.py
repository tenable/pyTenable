'''
GraphQL definitions file.
'''
from dataclasses import dataclass
from typing import List
from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow.schema import Schema


class GraphObject():
    '''
    A class wrapper for the GraphQL query.
    This class can be further wrapped with other GraphObject classes that
    add more functionality to the original query.
    '''

    def __init__(self, object_name, query, resp_schema, query_variables):
        self._object_name = object_name
        self._query = query
        self._resp_schema = resp_schema
        self._query_variables = query_variables

    @property
    def object_name(self):
        '''
        The name of the GraphQL object that appears in the query.
        '''
        return self._object_name

    @property
    def query(self):
        '''
        The GraphQL query.
        '''
        return self._query

    @property
    def resp_schema(self):
        '''
        The expected response schema from the query.
        '''
        return self._resp_schema

    @property
    def query_variables(self):
        '''
        The variables to pass to the query on call.
        '''
        return self._query_variables


class GraphqlParsingError(Exception):
    '''
    An error that's returned when a problem occurs parsing the Graphql response
    '''

    def __init__(self, message):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class LocationSchema(Schema):
    '''
    Schema for GraphQL location part of the error.
    '''
    line = fields.Int(required=True)
    column = fields.Int(required=True)

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Location(**data)


class ExtensionsSchema(Schema):
    '''
    Schema for GraphQL extensions part of the error.
    '''
    code = fields.Str()

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Extensions(**data)


class GraphqlErrorSchema(Schema):
    '''
    Schema for GraphQL error.
    '''
    message = fields.Str(required=True)
    locations = fields.List(fields.Nested(LocationSchema))
    path = fields.List(fields.Str())
    extensions = fields.Nested(ExtensionsSchema)

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return GraphqlError(**data)


@dataclass
class Location():
    '''
    This class holds the location part of the error.
    '''
    line: int
    column: int


@dataclass
class Extensions():
    '''
    This class holds the extensions part of the error.
    '''
    code: str = None


@dataclass
class GraphqlError(Exception):
    '''
    This class holds a GraphQL error.
    '''
    message: str
    locations: List[Location] = None
    path: List[str] = None
    extensions: Extensions = None

    def __str__(self):
        return '{ret_code}: {message} ({location}), path {path}'.format(
            ret_code=self.extensions.code,
            message=self.message,
            location=self.locations[0],
            path=self.path
        )
