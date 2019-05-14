from tenable.errors import *
from ..checker import check, single
import uuid, pytest

@pytest.mark.vcr()
def test_files_upload(api):
    api.files.upload('ExampleDataGoesHere')