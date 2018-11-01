from .fixtures import *
from tenable.errors import *
import uuid

def test_upload(api):
    api.files.upload('ExampleDataGoesHere')