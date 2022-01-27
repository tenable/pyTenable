'''
Testing the Attachments endpoints
'''
import os
import re

import pytest
import responses

ATTACHMENTS_BASE_URL = r'https://cloud.tenable.com/api/v3/was/attachments'
USERS_API_ID = r'([0-9a-fA-F\-]+)'

dir_name = os.path.dirname(os.path.abspath(__file__))

IMG_ATTACHMENT_FILE = 'img_attachment_file.png'
TXT_ATTACHMENT_FILE = 'text_attachment_file.txt'

IMG_ATTACHMENT_FILE_PATH = os.path.join(dir_name, IMG_ATTACHMENT_FILE)
TXT_ATTACHMENT_FILE_PATH = os.path.join(dir_name, TXT_ATTACHMENT_FILE)

IMG_ATTACHMENT_ID = 'b1b335cf-938f-462a-b83d-088b72428a2a'
TXT_ATTACHMENT_ID = '49484c93-baa5-4952-8043-9afad238cb7b'


@pytest.fixture
def image_contents():
    '''
    Fixture to read the contents of image file.
    '''

    with open(IMG_ATTACHMENT_FILE_PATH, 'rb') as img_file:
        image_data = img_file.read()

    return image_data


@pytest.fixture
def text_contents():
    '''
    Fixture to read the contents of text file.
    '''

    with open(TXT_ATTACHMENT_FILE_PATH, 'rb') as txt_file:
        text_data = txt_file.read()

    return text_data


@responses.activate
def test_download_img_attachment(image_contents, api):
    '''
    Test image attachment without File Object
    '''

    responses.add(
        responses.GET,
        re.compile(f'{ATTACHMENTS_BASE_URL}/{IMG_ATTACHMENT_ID}'),
        body=image_contents
    )

    resp = api.v3.was.attachments.download_attachment(IMG_ATTACHMENT_ID)
    assert resp.read() == image_contents


@responses.activate
def test_download_img_file_attachment(image_contents, api):
    '''
    Test image attachment with File Object
    '''

    responses.add(
        responses.GET,
        re.compile(f'{ATTACHMENTS_BASE_URL}/{IMG_ATTACHMENT_ID}'),
        body=image_contents
    )

    output_img_file_name = 'img_output_file.png'
    with open(output_img_file_name, 'wb') as img_file:
        api.v3.was.attachments.download_attachment(
            IMG_ATTACHMENT_ID,
            img_file
        )

    with open(output_img_file_name, 'rb') as img_output:
        assert img_output.read() == image_contents

    os.remove(output_img_file_name)


@responses.activate
def test_download_txt_attachment(text_contents, api):
    '''
    Test text attachment without File Object
    '''

    responses.add(
        responses.GET,
        re.compile(f'{ATTACHMENTS_BASE_URL}/{TXT_ATTACHMENT_ID}'),
        body=text_contents
    )

    resp = api.v3.was.attachments.download_attachment(TXT_ATTACHMENT_ID)
    assert resp.read() == text_contents


@responses.activate
def test_download_txt_file_attachment(text_contents, api):
    '''
    Test text attachment with File Object
    '''

    responses.add(
        responses.GET,
        re.compile(f'{ATTACHMENTS_BASE_URL}/{TXT_ATTACHMENT_ID}'),
        body=text_contents
    )

    output_txt_file_name = 'txt_output_file.txt'
    with open(output_txt_file_name, 'wb') as txt_file:
        api.v3.was.attachments.download_attachment(
            TXT_ATTACHMENT_ID,
            txt_file
        )

    with open(output_txt_file_name, 'rb') as txt_output:
        assert txt_output.read() == text_contents

    os.remove(output_txt_file_name)
