from .fixtures import *
from tenable.errors import *
import uuid

def test_upload(api):
    api.file.upload('ExampleDataGoesHere')