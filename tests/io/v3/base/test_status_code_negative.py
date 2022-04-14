'''
Test cases for Tenable.io API negative status codes
'''
import pytest
import responses
from restfly.errors import (BadRequestError, ForbiddenError, NotFoundError,
                            ServerError, TooManyRequestsError,
                            UnauthorizedError, InvalidMethodError, NotAcceptableError, RequestConflictError,
                            PayloadTooLargeError, UnsupportedMediaTypeError, ServiceUnavailableError,
                            MethodNotImplementedError)

error_codes = [
    (400, BadRequestError),
    (401, UnauthorizedError),
    (403, ForbiddenError),
    (404, NotFoundError),
    (405, InvalidMethodError),
    (406, NotAcceptableError),
    (409, RequestConflictError),
    (413, PayloadTooLargeError),
    (415, UnsupportedMediaTypeError),
    (429, TooManyRequestsError),
    (500, ServerError),
    (501, MethodNotImplementedError),
    (503, ServiceUnavailableError)
]
BASE_URL = 'https://cloud.tenable.com/api/v3/was'
SAMPLE_ID = 'cade336b-29fb-4188-b42a-04d8f95d7de6'
TEST_IDS = [code[0] for code in error_codes]


@responses.activate
@pytest.mark.parametrize('error_codes', error_codes, ids=TEST_IDS)
def test_status_code_get(api, error_codes):
    '''
    Negative status code scenario for GET request
    '''
    responses.add(
        responses.GET,
        f'{BASE_URL}/scans/{SAMPLE_ID}',
        status=error_codes[0]
    )

    with pytest.raises(error_codes[1]):
        api.v3.was.scans.details(SAMPLE_ID)


@responses.activate
@pytest.mark.parametrize('error_codes', error_codes, ids=TEST_IDS)
def test_status_code_post(api, error_codes):
    '''
    Negative status code scenario for POST request
    '''
    responses.add(
        responses.POST,
        f'{BASE_URL}/configs/{SAMPLE_ID}/scans',
        status=error_codes[0]
    )

    with pytest.raises(error_codes[1]):
        api.v3.was.scans.launch(SAMPLE_ID)


@responses.activate
@pytest.mark.parametrize('error_codes', error_codes, ids=TEST_IDS)
def test_status_code_put(api, error_codes):
    '''
    Negative status code scenario for PUT request
    '''
    responses.add(
        responses.PUT,
        f'{BASE_URL}/scans/{SAMPLE_ID}/report',
        status=error_codes[0]
    )

    with pytest.raises(error_codes[1]):
        api.v3.was.scans.export(SAMPLE_ID)


@responses.activate
@pytest.mark.parametrize('error_codes', error_codes, ids=TEST_IDS)
def test_status_code_delete(api, error_codes):
    '''
    Negative status code scenario for DELETE request
    '''
    responses.add(
        responses.DELETE,
        f'{BASE_URL}/scans/{SAMPLE_ID}',
        status=error_codes[0]
    )

    with pytest.raises(error_codes[1]):
        api.v3.was.scans.delete(SAMPLE_ID)


@responses.activate
@pytest.mark.parametrize('error_codes', error_codes, ids=TEST_IDS)
def test_status_code_patch(api, error_codes):
    '''
    Negative status code scenario for PATCH request
    '''
    responses.add(
        responses.PATCH,
        f'{BASE_URL}/scans/{SAMPLE_ID}',
        status=error_codes[0]
    )

    with pytest.raises(error_codes[1]):
        api.v3.was.scans.update_status(SAMPLE_ID, 'stop')
