"""
test for uploading the file and file with encryption
"""
import os
import uuid
import pytest


@pytest.mark.vcr()
def test_files_upload(api):
    """
    test to uploads the file object
    """
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        '..', 'test_files', f'test-upload-{str(uuid.uuid4())}.txt')

    with open(file, 'w+') as fobj:
        fobj.write('test')
        fobj.close()

    try:
        with open(file, 'rb') as fobj:
            api.files.upload(fobj)
    except:
        raise
    finally:
        os.remove(file)


@pytest.mark.vcr()
def test_files_encryption_success(api, datafiles):
    """
    test to upload the file with encryption
    """
    file = f'test-upload-{str(uuid.uuid4())}.txt'
    with open(os.path.join(str(datafiles), file), 'w+') as fobj:
        fobj.write('test')
        fobj.close()
    with open(os.path.join(str(datafiles), file), 'rb') as fobj:
        api.files.upload(fobj, encrypted=True)