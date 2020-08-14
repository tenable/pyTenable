'''
Base Endpoint
=============

The APIEndpoint class is the base class that all endpoint modules will inherit
from.  Throughout pyTenable v1, packages will be transitioning to using this
base class over the original APISession class.

.. autoclass:: APIEndpoint
    :members:
    :inherited-members:
'''
from restfly import APIEndpoint as Base

class APIEndpoint(Base):
    pass