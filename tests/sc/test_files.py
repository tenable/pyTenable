import os
import pytest


@pytest.mark.vcr()
def test_files_upload_clear_success(sc):
    with open('1000003.xml', 'w+') as file:
        response = sc.files.upload(fobj=file)
        filename = sc.files.clear(response)
        assert filename == 'filename'
    os.remove('1000003.xml')
