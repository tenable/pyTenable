'''
Test cases for Logos API
'''
import os
import uuid

import pytest
import responses

# from responses import matchers

LOGOS_BASE_URL = r'https://cloud.tenable.com/api/v3/mssp/logos'
BASE_URL = r'https://cloud.tenable.com'
LOGO_ID = str(uuid.uuid1())
LOGO_PATH = 'pyTenable\\tests\\io\\v3\\vm\\logos\\test_image.png'
LOGO_PATH = os.path.join(
    os.getcwd(),
    os.path.dirname(__file__),
    'test_image.png'
)


@responses.activate
def test_add(api):
    file_obj = open(LOGO_PATH, 'rb')
    name = 'Image_name'
    api_resp = {'id': '336995a8-0f32-43a2-a134-2261657cd102'}
    # payload = {'files': {'logo': file_obj, 'name': name}}
    responses.add(
        responses.POST,
        LOGOS_BASE_URL,
        # match=[matchers.json_params_matcher(payload)],
        json=api_resp
    )
    resp = api.v3.vm.logos.add(file_obj, name)
    assert resp == api_resp


def test_search(api):
    '''
    Test case for validating search action of Logos API
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.logos.search()


@responses.activate
def test_delete(api):
    responses.add(
        responses.DELETE,
        f'{LOGOS_BASE_URL}/{LOGO_ID}',
    )
    assert api.v3.vm.logos.delete(LOGO_ID) is None


@responses.activate
def test_details(api):
    api_resp = {
        'id': LOGO_ID,
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'name': 'download1.png',
        'filename': 'download1.png'
    }
    responses.add(
        responses.GET,
        f'{LOGOS_BASE_URL}/{LOGO_ID}',
        json=api_resp
    )
    resp = api.v3.vm.logos.details(LOGO_ID)
    assert resp == api_resp
