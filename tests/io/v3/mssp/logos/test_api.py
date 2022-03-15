'''
Test cases for Logos API
'''
import os
import uuid

import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

LOGOS_BASE_URL = r'https://cloud.tenable.com/api/v3/mssp/logos'
BASE_URL = r'https://cloud.tenable.com'
LOGO_ID = str(uuid.uuid1())
LOGO_PATH = os.path.join(
    os.getcwd(),
    os.path.dirname(__file__),
    'test_image.png'
)


@responses.activate
def test_add(api):
    '''
    Test case for validating add action for Logos API
    '''
    file_obj = open(LOGO_PATH, 'rb')
    name = 'Image_name'
    api_resp = {'id': '336995a8-0f32-43a2-a134-2261657cd102'}
    responses.add(
        responses.POST,
        LOGOS_BASE_URL,
        json=api_resp
    )
    resp = api.v3.mssp.logos.add(file_obj, name)
    assert resp == api_resp['id']


@responses.activate
def test_search(api):
    '''
    Test the search functionality of Logos API
    '''
    fields = [
        'container_id',
        'id',
        'name',
        'filename'
    ]

    payload = {
        'fields': fields,
        'limit': 200
    }

    api_response = {
        "logos": [{
            "id": "1028c13f-9cb5-40ec-a1a4-a458b21ae2f7",
            "container_id": "cfdabb09-6aef-481d-b28f-aecb1c38f297",
            "name": "download27.png",
            "filename": "download1.png"
        }, {
            "id": "0cba902a-bd11-4481-bd28-999c88ffe22f",
            "container_id": "cfdabb09-6aef-481d-b28f-aecb1c38f297",
            "name": "profile.png",
            "filename": "download27.png"
        }],
        "pagination": {
            "total": 2,
            "next": "nextToken"
        }
    }

    responses.add(
        responses.POST,
        f'{LOGOS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.mssp.logos.search(
        fields=fields, limit=200
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.mssp.logos.search(
        fields=fields, return_csv=True, limit=200
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.mssp.logos.search(
        fields=fields, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)


@responses.activate
def test_delete(api):
    '''
    Test case for validating delete action for Logos API
    '''
    responses.add(
        responses.DELETE,
        f'{LOGOS_BASE_URL}/{LOGO_ID}',
    )
    assert api.v3.mssp.logos.delete(LOGO_ID) is None


@responses.activate
def test_details(api):
    '''
    Test case for validating details action for Logos API
    '''
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
    resp = api.v3.mssp.logos.details(LOGO_ID)
    assert resp == api_resp


@responses.activate
def test_assign_logos(api):
    '''
    Test case for validating assign_logos action for Logos API
    '''
    account_ids = ['0fc4ef49-2649-4c76-bfa7-c181be3adf26']
    payload = {
        'account_ids': account_ids,
        'logo_id': LOGO_ID
    }
    responses.add(
        responses.PUT,
        f'{BASE_URL}/api/v3/mssp/accounts/logos',
        match=[matchers.json_params_matcher(payload)]
    )
    assert api.v3.mssp.logos.assign_logos(LOGO_ID, account_ids) is None


@responses.activate
def test_update(api):
    '''
    Test case for validating update action for Logos API
    '''
    api_resp = {'id': LOGO_ID}
    f1 = open(LOGO_PATH, 'rb')
    responses.add(
        responses.PATCH,
        f'{LOGOS_BASE_URL}/{LOGO_ID}',
        json=api_resp
    )
    resp = api.v3.mssp.logos.update(LOGO_ID, logo=f1, name='test_image.png')
    assert resp == api_resp['id']


@responses.activate
def test_donwload_png(api):
    '''
    Test case for validating donwload_png action for Logos API
    '''
    PATH = LOGO_PATH.replace('test_image', 'test_download')
    with open(LOGO_PATH, 'rb') as fobj:
        file_contents = fobj.read()
    responses.add(
        responses.GET,
        f'{LOGOS_BASE_URL}/{LOGO_ID}/logo.png',
        body=file_contents
    )
    with open(PATH, 'wb') as f1:
        api.v3.mssp.logos.download_png(LOGO_ID, fobj=f1)

    with open(PATH, 'rb') as fobj:
        assert file_contents == fobj.read()
    os.remove(PATH)

    # Validate the method when fileObj is not passed
    assert file_contents == api.v3.mssp.logos.download_png(LOGO_ID).read()


@responses.activate
def test_donwload_base64(api):
    '''
    Test case for validating donwload_base64 action for Logos API
    '''
    api_resp = b'data:image/png;base64,kjdbsfkabfksdbf'
    responses.add(
        responses.GET,
        f'{LOGOS_BASE_URL}/{LOGO_ID}/logo.base64',
        body=api_resp
    )
    resp = api.v3.mssp.logos.download_base64(LOGO_ID)
    assert resp == api_resp
