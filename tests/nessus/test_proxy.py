import pytest
import responses


@responses.activate
def test_proxy_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/settings/network/proxy'
                  )
    nessus.proxy.edit(proxy='proxy.company.com',
                      proxy_auth='auto',
                      proxy_password='password',
                      proxy_username='username',
                      proxy_port=8080,
                      user_agent='Proxy UserAgent'
                      )


@responses.activate
def test_proxy_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/network/proxy',
                  json={
                    'proxy': 'proxy.company.com',
                    'proxy_auth': 'basic',
                    'proxy_password': '1234567890',
                    'proxy_username': 'user',
                    'proxy_port': 8080,
                    'user_agent': 'Awesome Useragent'
                  })
    resp = nessus.proxy.details()
    assert isinstance(resp, dict)
    assert resp['proxy'] == 'proxy.company.com'
    