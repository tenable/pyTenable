import logging

import arrow
import pytest
import responses
from box import Box, BoxList
from requests import Response
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util.retry import Retry

from tenable import errors
from tenable.base._restfly_v1 import (
    APIEndpoint,
    APIIterator,
    APISession,
    check,
    dict_clean,
    dict_flatten,
    dict_merge,
    force_case,
    redact_values,
    trunc,
    url_validator,
)


@pytest.fixture
def api():
    return APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='1.5.2-embedded',
    )


@pytest.fixture
def e(api):
    return APIEndpoint(api)


def validate_endpoint(e, api):
    assert e._api == api
    assert e._log == api._log


@responses.activate
def test_endpoint_delete(e):
    responses.add(responses.DELETE, 'https://httpbin.org/delete')
    resp = e._delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_head(e):
    responses.add(responses.HEAD, 'https://httpbin.org')
    resp = e._head('')
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_get(e):
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = e._get('get', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_patch(e):
    responses.add(responses.PATCH, 'https://httpbin.org/patch')
    resp = e._patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_post(e):
    responses.add(responses.POST, 'https://httpbin.org/post')
    resp = e._post('post', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_put(e):
    responses.add(responses.PUT, 'https://httpbin.org/put')
    resp = e._put('put', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_base_request(e):
    responses.add(responses.PUT, 'https://httpbin.org/put', json={'test': 'value'})
    resp = e._req('PUT', 'put', json={'test': 'value'})
    assert isinstance(resp, Response)

    # Test endpoint params:
    e._box = True
    e._box_attrs = {'default_box': True}
    assert isinstance(e._req('PUT', 'put', json={'test': 'value'}), Box)

    e._box = None
    e._conv_json = True
    assert isinstance(e._req('PUT', 'put', json={'test': 'value'}), dict)


@responses.activate
def test_endpoint_path_get(api):
    responses.add(responses.GET, 'https://httpbin.org/get')

    class TestAPI(APIEndpoint):
        _path = 'get'

        def get(self):
            return self._get()

    endpoint = TestAPI(api)
    resp = endpoint.get()
    assert isinstance(resp, Response)


class ExampleIterator(APIIterator):
    limit = 10
    offset = 0

    def _get_page(self):
        self.total = 100
        self.page = [{'id': i + self.offset} for i in range(self.limit)]
        self.offset += self.limit


def test_iterator_stubs():
    assert APIIterator(None)._get_page() is None


def test_iterator_get_key():
    items = ExampleIterator(None)
    items.next()
    assert items.get(0) == {'id': 0}
    assert items[0] == {'id': 0}
    assert items.get(101, None) is None


def test_blank_page():
    class ExIterator(APIIterator):
        page = []

    with pytest.raises(StopIteration):
        ExIterator(None).next()


def test_iterator():
    items = ExampleIterator(None)
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {'id': 99}
    assert items.total == 100
    assert items.count == 100
    assert items.num_pages == 10
    assert items.page_count == 10
    assert items.page == [
        {'id': 90},
        {'id': 91},
        {'id': 92},
        {'id': 93},
        {'id': 94},
        {'id': 95},
        {'id': 96},
        {'id': 97},
        {'id': 98},
        {'id': 99},
    ]


def test_iterator_max_items():
    items = ExampleIterator(None, max_items=15)
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {'id': 14}
    assert items.total == 100
    assert items.count == 15
    assert items.num_pages == 2
    assert items.page_count == 5
    assert items.page == [
        {'id': 10},
        {'id': 11},
        {'id': 12},
        {'id': 13},
        {'id': 14},
        {'id': 15},
        {'id': 16},
        {'id': 17},
        {'id': 18},
        {'id': 19},
    ]


def test_iterator_max_pages():
    items = ExampleIterator(None, max_pages=2)
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {'id': 19}
    assert items.total == 100
    assert items.count == 20
    assert items.num_pages == 2
    assert items.page_count == 10
    assert items.page == [
        {'id': 10},
        {'id': 11},
        {'id': 12},
        {'id': 13},
        {'id': 14},
        {'id': 15},
        {'id': 16},
        {'id': 17},
        {'id': 18},
        {'id': 19},
    ]


def test_error_repr():
    err = errors.RestflyException('This is a test')
    assert str(err) == 'This is a test'
    assert err.__repr__() == "'This is a test'"


def test_retriable_error():
    assert errors.APIError.retryable is False
    errors.APIError.set_retryable(True)
    assert errors.APIError.retryable is True
    errors.APIError.set_retryable(False)
    assert errors.APIError.retryable is False


def test_user_agent_string(api):
    ua = 'Integration/1.0 (pytest; auto-test; Build/1.5.2-embedded)'
    assert ua in api._session.headers['User-Agent']


def test_unexpected_keys_error():
    class Example1(APISession):
        _error_on_unexpected_input = True
        _url = 'https://httpbin.org'

    class Example2(APISession):
        _error_on_unexpected_input = False
        _url = 'https://httpbin.org'

    # should raise an error with the invalid KW
    with pytest.raises(errors.UnexpectedValueError):
        Example1(something=True)

    # Should not raise the error and just ignore it.
    Example2(something=True)


def test_example_context_manager():
    """
    This test creates a simple "authentication" to validate that the
    context management is actually working as expected.  As the _authenticate
    method is automatically run when entering the context, and _deauthenticate
    is run upon exit, we will simply be modifying the authed variable in the
    outer scope and asserting that its being properly set.
    """
    global authed

    class Example(APISession):
        _url = 'https://httpbin.org'

        def _authenticate(self, **kwargs):
            global authed
            authed = True

        def _deauthenticate(self):
            global authed
            authed = False

    with Example():
        assert authed is True
    assert authed is False


def test_session_proxies():
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='1.5.2-embedded',
        proxies={'http': 'localhost:8080'},
    )
    assert api._session.proxies == {'http': 'localhost:8080'}


def test_session_ssl_validation():
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='1.5.2-embedded',
        ssl_verify=False,
    )
    assert api._session.verify is False


def test_client_ssl_cert():
    cert_tuple = ('/path/to/cert.crt', '/path/to/cert.key')
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='1.5.2-embedded',
        cert=cert_tuple,
    )
    assert api._session.cert == cert_tuple


def test_session_adapter():
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=5,
    )
    adapter = HTTPAdapter(max_retries=retry)
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='1.5.2-embedded',
        adapter=adapter,
    )
    assert api._session.get_adapter('https://httpbin.org/') == adapter


def test_session_stubs(api):
    api._authenticate()
    api._deauthenticate()


@responses.activate
def test_session_delete(api):
    responses.add(responses.DELETE, 'https://httpbin.org/delete')
    resp = api.delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_get(api):
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = api.get('get', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_patch(api):
    responses.add(responses.PATCH, 'https://httpbin.org/patch')
    resp = api.patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_post(api):
    responses.add(responses.POST, 'https://httpbin.org/post')
    resp = api.post('post', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_put(api):
    responses.add(responses.PUT, 'https://httpbin.org/put')
    resp = api.put('put', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_head(api):
    responses.add(responses.HEAD, 'https://httpbin.org/')
    resp = api.head('')
    assert isinstance(resp, Response)


@responses.activate
def test_session_redirect(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/redirect-to',
        status=302,
        headers={'Location': '/get'},
    )
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = api.get('redirect-to', params={'url': '/get'})
    assert isinstance(resp, Response)
    assert resp.url == 'https://httpbin.org/get'


@responses.activate
def test_debug_logging(api, caplog):
    logger = 'tenable.base._restfly_v1.APISession'
    data = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}}
    responses.add(responses.POST, 'https://httpbin.org/post', json={'json': data})
    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger=logger):
        resp = api.post('post', json=data, redact_fields=['a', 'd'], box=False)
        assert '"a": "REDACTED"' in caplog.text
        assert '"d": "REDACTED"' in caplog.text
        assert resp.json()['json'] == data

    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger=logger):
        api._restricted_paths = ['post']
        resp = api.post('post', json=data, redact_fields=['a', 'd'], box=False)
        api._restricted_paths = []
        assert '"params": "REDACTED"' in caplog.text
        assert '"body": "REDACTED"' in caplog.text
        assert resp.json()['json'] == data

    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger=logger):
        resp = api.post('post', json=data, box=False)
        assert 'REDACTED' not in caplog.text
        assert resp.json()['json'] == data


@responses.activate
def test_session_full_uri(api):
    responses.add(responses.GET, 'https://httpbin.org/get', json={'test': 'value'})
    resp1 = api.get('get').json()
    resp2 = api.get('https://httpbin.org/get').json()
    assert resp1 == resp2


@responses.activate
def test_session_base_path(api):
    responses.add(
        responses.POST, 'https://httpbin.org/post', json={'data': {'test': 'value'}}
    )
    resp1 = api.post('post', json={'test': 'value'}).json()
    api._base_path = 'get'
    resp2 = api.post('post', json={'test': 'value'}, use_base=False).json()
    resp1['headers'] = {}
    resp2['headers'] = {}
    assert resp1 == resp2

    responses.add(responses.GET, 'https://httpbin.org/status/200')
    api._base_path = 'status'
    api.get('200')


@responses.activate
def test_session_retry_after(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/response-headers',
        headers={'Retry-After': '.1'},
    )
    api.get('response-headers', params={'Retry-After': 1})


def test_session_ssl_error(api):
    with pytest.raises(SSLError):
        api.get('https://self-signed.badssl.com/')
    api._ssl_verify = False
    with pytest.warns(InsecureRequestWarning):
        api.get('https://self-signed.badssl.com/')


@responses.activate
def test_session_badrequesterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/400', status=400)
    with pytest.raises(errors.BadRequestError):
        api.get('status/400')


@responses.activate
def test_session_unauthorizederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/401', status=401)
    with pytest.raises(errors.UnauthorizedError):
        api.get('status/401')


@responses.activate
def test_session_forbiddenerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/403', status=403)
    with pytest.raises(errors.ForbiddenError):
        api.get('status/403')


@responses.activate
def test_session_notfounderror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/404', status=404)
    with pytest.raises(errors.NotFoundError):
        api.get('status/404')


@responses.activate
def test_session_invalidmethoderror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/405', status=405)
    with pytest.raises(errors.InvalidMethodError):
        api.get('status/405')


@responses.activate
def test_session_notacceptableerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/406', status=406)
    with pytest.raises(errors.NotAcceptableError):
        api.get('status/406')


@responses.activate
def test_session_proxyauthenticationerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/407', status=407)
    with pytest.raises(errors.ProxyAuthenticationError):
        api.get('status/407')


@responses.activate
def test_session_requesttimeouterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/408', status=408)
    with pytest.raises(errors.RequestTimeoutError):
        api.get('status/408')


@responses.activate
def test_session_requestconflicterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/409', status=409)
    with pytest.raises(errors.RequestConflictError):
        api.get('status/409')


@responses.activate
def test_session_nolongerexistserror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/410', status=410)
    with pytest.raises(errors.NoLongerExistsError):
        api.get('status/410')


@responses.activate
def test_session_lengthrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/411', status=411)
    with pytest.raises(errors.LengthRequiredError):
        api.get('status/411')


@responses.activate
def test_session_preconditionfailederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/412', status=412)
    with pytest.raises(errors.PreconditionFailedError):
        api.get('status/412')


@responses.activate
def test_session_payloadtoolargeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/413', status=413)
    with pytest.raises(errors.PayloadTooLargeError):
        api.get('status/413')


@responses.activate
def test_session_uritoolongerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/414', status=414)
    with pytest.raises(errors.URITooLongError):
        api.get('status/414')


@responses.activate
def test_session_unsupportedmediatypeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/415', status=415)
    with pytest.raises(errors.UnsupportedMediaTypeError):
        api.get('status/415')


@responses.activate
def test_session_rangenotsatisfiableerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/416', status=416)
    with pytest.raises(errors.RangeNotSatisfiableError):
        api.get('status/416')


@responses.activate
def test_session_expectationfailederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/417', status=417)
    with pytest.raises(errors.ExpectationFailedError):
        api.get('status/417')


@responses.activate
def test_session_teapotresponseerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/418', status=418)
    with pytest.raises(errors.TeapotResponseError):
        api.get('status/418')


@responses.activate
def test_session_misdirectrequesterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/421', status=421)
    with pytest.raises(errors.MisdirectRequestError):
        api.get('status/421')


@responses.activate
def test_session_tooearlyerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/425', status=425)
    with pytest.raises(errors.TooEarlyError):
        api.get('status/425')


@responses.activate
def test_session_upgraderequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/426', status=426)
    with pytest.raises(errors.UpgradeRequiredError):
        api.get('status/426')


@responses.activate
def test_session_preconditionrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/428', status=428)
    with pytest.raises(errors.PreconditionRequiredError):
        api.get('status/428')


@responses.activate
def test_session_toomanyrequests(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/429',
        status=429,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.TooManyRequestsError):
        api.get('status/429')


@responses.activate
def test_session_requestheaderfieldstoolargeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/431', status=431)
    with pytest.raises(errors.RequestHeaderFieldsTooLargeError):
        api.get('status/431')


@responses.activate
def test_session_unavailableforlegalreasonserror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/451', status=451)
    with pytest.raises(errors.UnavailableForLegalReasonsError):
        api.get('status/451')


@responses.activate
def test_session_servererror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/500', status=500)
    with pytest.raises(errors.ServerError):
        api.get('status/500')


@responses.activate
def test_session_methodnotimplimentederror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/501',
        status=501,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.MethodNotImplementedError):
        api.get('status/501')


@responses.activate
def test_session_badgatewayerror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/502',
        status=502,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.BadGatewayError):
        api.get('status/502')


@responses.activate
def test_session_serviceunavailableerror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/503',
        status=503,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.ServiceUnavailableError):
        api.get('status/503')


@responses.activate
def test_session_gatewaytimeouterror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/504',
        status=504,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.GatewayTimeoutError):
        api.get('status/504')


@responses.activate
def test_session_notextendederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/510', status=510)
    with pytest.raises(errors.NotExtendedError):
        api.get('status/510')


@responses.activate
def test_session_networkauthrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/511', status=511)
    with pytest.raises(errors.NetworkAuthenticationRequiredError):
        api.get('status/511')


@responses.activate
def test_session_catchall_error(api):
    responses.add(responses.GET, 'https://httpbin.org/status/555', status=555)
    with pytest.raises(errors.APIError):
        api.get('status/555')


@responses.activate
def test_session_box_non_json(api):
    html_body = '<html><head></head><body><h1>Hello World</h1></body></html>'
    responses.add(
        responses.GET,
        'https://httpbin.org/html',
        headers={'Content-Type': 'text/html; charset=utf-8'},
        body=html_body,
    )
    assert isinstance(api.get('html', box=True), Response)


@responses.activate
def test_session_box_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', box=True), Box)
    responses.add(
        responses.GET,
        'https://httpbin.org/json',
        json=[{'test': 'value'} for _ in range(20)],
    )
    assert isinstance(api.get('json', box=True), BoxList)


@responses.activate
def test_session_disable_box(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', box=False), Response)


@responses.activate
def test_session_conv_json_non_json(api):
    html_body = '<html><head></head><body><h1>Hello World</h1></body></html>'
    responses.add(
        responses.GET,
        'https://httpbin.org/html',
        headers={'Content-Type': 'text/html; charset=utf-8'},
        body=html_body,
    )
    assert isinstance(api.get('html', conv_json=True), Response)


@responses.activate
def test_session_conv_json_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', conv_json=True), dict)


@responses.activate
def test_session_disable_conv_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', conv_json=False), Response)


def test_force_case_single():
    assert force_case('TEST', 'lower') == 'test'
    assert force_case('test', 'upper') == 'TEST'


def test_force_case_list():
    assert force_case(['a', 'b', 'c'], 'upper') == ['A', 'B', 'C']
    assert force_case(['A', 'B', 'C'], 'lower') == ['a', 'b', 'c']


def test_dict_merge():
    with pytest.deprecated_call():
        assert dict_merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
        assert dict_merge({'s': {'a': 1}, 'b': 2}, {'s': {'c': 3, 'a': 4}}) == {
            's': {'a': 4, 'c': 3},
            'b': 2,
        }
        assert dict_merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 5}) == {
            'a': 5,
            'b': 2,
            'c': 3,
        }


def test_dict_flatten():
    assert dict_flatten({'a': 1, 'b': {'c': 2}}) == {'a': 1, 'b.c': 2}
    assert dict_flatten({'A': 1, 'B': {'c': 2}}, lower_key=True) == {'a': 1, 'b.c': 2}
    assert dict_flatten({'a': 1, 'b': [{'c': 2, 'd': {'e': 1}}]}) == {
        'a': 1,
        'b': [{'c': 2, 'd.e': 1}],
    }


def test_dict_clean():
    dirty = {
        'a': 1,
        'b': {'c': 2, 'd': None},
        'e': None,
        'f': [{'g': 1, 'h': None}, {'i': None}],
        'j': [1, None, {}],
    }
    assert dict_clean(dirty) == {'a': 1, 'b': {'c': 2}, 'f': [{'g': 1}], 'j': [1, None]}


def test_trunc():
    assert trunc('Hello There!', 128) == 'Hello There!'
    assert trunc('Too Small', 6) == 'Too...'
    assert trunc('Too Small', 3, suffix=None) == 'Too'


examples = {
    'uuid': '00000000-0000-0000-0000-000000000000',
    'email': 'someone@company.tld',
    'hex': '1234567890abcdef',
    'url': 'http://company.com/path/of/stuff',
    'ipv4': '192.168.0.1',
    'ipv6': '2001:0db8:0000:0000:0000:ff00:0042:8329',
}


def test_check_single_type():
    assert isinstance(check('test', 1, int), int)


def test_check_list_items_type():
    assert isinstance(check('test', [1, 2], list, items_type=int), list)


def test_check_single_type_soft_checking():
    assert isinstance(check('test', '1', int), int)


def test_check_single_type_softcheck_fail():
    with pytest.raises(TypeError):
        check('test', '1', int, softcheck=False)


def test_check_type_fail():
    with pytest.raises(TypeError):
        check('test', 1, str)


def test_check_list_items_fail():
    with pytest.raises(TypeError):
        check('test', [1, 2, 'three'], list, items_type=int)


def test_check_list_items_softcheck():
    assert check('test', [1, 2, '3'], list, items_type=int) == [1, 2, 3]


def test_check_choices():
    check('test', [1, 2, 3], list, choices=list(range(5)))


def test_check_choices_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', [1, 2, 3, 500], list, choices=list(range(5)))


def test_check_pattern_mapping_uuid():
    check('test', examples['uuid'], str, pattern='uuid')


def test_check_pattern_mapping_uuid_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, pattern='uuid')


def test_check_pattern_mapping_email():
    check('test', examples['email'], str, pattern='email')


def test_check_pattern_mapping_email_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, pattern='email')


def test_check_pattern_mapping_hex():
    check('test', examples['hex'], str, pattern='hex')


def test_check_pattern_mapping_hex_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'something', str, pattern='hex')


def test_check_pattern_mapping_url():
    check('test', examples['url'], str, pattern='url')


def test_check_pattern_mapping_url_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, pattern='url')


def test_check_pattern_mapping_ipv4():
    check('test', examples['ipv4'], str, pattern='ipv4')


def test_check_pattern_mapping_ipv4_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv4')


def test_check_pattern_mapping_ipv6():
    check('test', examples['ipv6'], str, pattern='ipv6')


def test_check_pattern_mapping_ipv6_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv6')


def test_check_regex_pattern():
    check('test', '12345', str, regex=r'^\d+$')


def test_check_pattern_int_pass():
    check('test', 1, (int, str), pattern='ipv4')


def test_check_regex_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', 'abcdef', str, regex=r'^\d+$')


def test_check_allow_none_fail():
    with pytest.raises(errors.UnexpectedValueError):
        check('test', None, str, allow_none=False)


def test_arrow_type_inputs():
    arw = arrow.utcnow().floor('hour')

    # Test a floating point
    assert check('test', arw.timestamp(), arrow.Arrow) == arw

    # Test an integer
    assert check('test', int(arw.timestamp()), arrow.Arrow) == arw

    # Test a string
    assert check('test', arw.format(), arrow.Arrow) == arw

    # Test an arrow obj
    assert check('test', arw, arrow.Arrow) == arw


def test_bool_softchecks():
    assert check('test', 'yes', bool) is True
    assert check('test', 'true', bool) is True
    assert check('test', 'TRUE', bool) is True
    assert check('test', 'false', bool) is False
    assert check('test', 'FALSE', bool) is False
    assert check('test', 'no', bool) is False


def test_return_defaults():
    assert check('test', None, int) is None
    assert check('test', None, int, default=1) == 1


def test_pattern_map_failure():
    with pytest.raises(IndexError):
        check('test', 'something', str, pattern='something')


def test_url_validator():
    assert url_validator('https://google.com') is True
    assert (
        url_validator('https://httpbin.org/404', validate=['scheme', 'netloc', 'path'])
        is True
    )
    assert (
        url_validator('https://httpbin.org', validate=['scheme', 'netloc', 'path'])
        is False
    )
    assert url_validator('httpbin.org') is False


def test_redact_values():
    test = {'a': 1, 'b': 2, 'c': 3, 'd': {'e': 4, 'f': 5, 'g': 6}}
    assert redact_values(test, keys=['a', 'c', 'd', 'e']) == {
        'a': 'REDACTED',
        'b': 2,
        'c': 'REDACTED',
        'd': {'e': 'REDACTED', 'f': 5, 'g': 6},
    }
    assert redact_values(test) == test
