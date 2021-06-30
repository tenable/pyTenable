"""
Testing downloads functionality
"""

import re
import warnings
from io import BytesIO
import responses
import pytest

from tenable.dl import Downloads



def test_downloads_init(monkeypatch):
    '''
    Various class init tests
    '''
    warnings.simplefilter('always')
    # Test warning when no api token is set
    monkeypatch.delenv('TDL_API_TOKEN', False)
    with pytest.warns(Warning):
        download = Downloads()

    # Test that API token is being set properly with envvars
    monkeypatch.setenv('TDL_API_TOKEN', 'something')
    download = Downloads()
    assert download._session.headers.get('authorization') == 'Bearer something'
    monkeypatch.delenv('TDL_API_TOKEN')

    # Test that API token is being set properly when being passed
    download = Downloads(api_token='something')
    assert download._session.headers.get('authorization') == 'Bearer something'


@responses.activate
def test_list():
    '''
    Test for the list method.
    '''
    body=[
        {
            'title': 'Nessus',
            'page_slug': 'nessus',
            'description': 'Download Nessus and Nessus Manager.',
            'files_index_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus'
        }, {
            'title': 'Nessus Agents',
            'page_slug': 'nessus-agents',
            'description': 'Download Nessus Agents for use with Tenable.io and Nessus Manager',
            'files_index_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus-agents'
        }
    ]
    responses.add(
        method='GET',
        url='https://www.tenable.com:443/downloads/api/v2/pages',
        json=body
    )
    download = Downloads()
    res = download.list()
    assert len(res) == 2
    assert res[0].title == 'Nessus'
    assert res[0].page_slug == 'nessus'
    assert res[0].description == 'Download Nessus and Nessus Manager.'
    assert res[0].files_index_url == 'https://www.tenable.com/downloads/api/v2/pages/nessus'


@responses.activate
def test_details():
    '''
    Test for the details method.
    '''
    body = {
        'releases': {
            'Nessus - 6.12.1': [
                {
                    'file': 'Nessus-6.12.1-x64.msi',
                    'file_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-6.12.1-x64.msi',
                    'md5': 'afa36d16ae157497751fc24d837f261b',
                    'product_release_date': '08/15/2019',
                    'release_date': '08/12/2019',
                    'sha256': '22d934b35e7fc774289ab28f0b2dbad1c00348cb7d7512fe6bfff5d72352da6b',
                    'size': 91706368,
                    'version': '6.12.1'
                }, {
                    'file': 'nessus-updates-6.12.1.tar.gz',
                    'file_url': \
                        'https://www.tenable.com/downloads/api/v2/pages/nessus/files/nessus-updates-6.12.1.tar.gz',
                    'md5': 'b8e5c6f4298ddf136f82f9b0d8315335',
                    'product_release_date': '08/15/2019',
                    'release_date': '08/12/2019',
                    'sha256': '8be351f4c07a736598d752b1334d12309372ccd5ace4fe3f111631d867659692',
                    'size': 1446835260,
                    'version': '6.12.1'
                },
            ],
            'latest': {
                'Nessus - 6.12.1': [
                    {
                        'file': 'Nessus-6.12.1-x64.msi',
                        'file_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-6.12.1-x64.msi',
                        'md5': 'afa36d16ae157497751fc24d837f261b',
                        'product_release_date': '08/15/2019',
                        'release_date': '08/12/2019',
                        'sha256': '22d934b35e7fc774289ab28f0b2dbad1c00348cb7d7512fe6bfff5d72352da6b',
                        'size': 91706368,
                        'version': '6.12.1'
                    }, {
                        'file': 'nessus-updates-6.12.1.tar.gz',
                        'file_url': \
                            'https://www.tenable.com/downloads/api/v2/pages/nessus/files/nessus-updates-6.12.1.tar.gz',
                        'md5': 'b8e5c6f4298ddf136f82f9b0d8315335',
                        'product_release_date': '08/15/2019',
                        'release_date': '08/12/2019',
                        'sha256': '8be351f4c07a736598d752b1334d12309372ccd5ace4fe3f111631d867659692',
                        'size': 1446835260,
                        'version': '6.12.1'
                    },
                ],
            },
        },
        'signing_keys': [
            {
                'file': 'RPM-GPG-KEY-Tenable-2048',
                'file_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus/files/tenable-2048.gpg',
                'md5': '219b081542068d7e48bb5355dad4c5c8',
                'sha256': '0f407c2df84f925acd9822e26731f3a881b3b94e5931a2ff8bf43b47be59f11e',
                'size': 1764
            }, {
                'file': 'RPM-GPG-KEY-Tenable-1024',
                'file_url': 'https://www.tenable.com/downloads/api/v2/pages/nessus/files/tenable-1024.gpg',
                'md5': '9004c2bfd0c3dcfd2fbf24405988e18b',
                'sha256': '0f66921483806f1b3a8531bcd69f7e8711a7f0d3fc0b5ce7feb66abab32e1a7e',
                'size': 1390
            }
        ]
    }
    responses.add(
        method='GET',
        url='https://www.tenable.com:443/downloads/api/v2/pages/nessus',
        json=body
    )
    download = Downloads()
    test_res = download.details('nessus')
    assert test_res.releases
    keys = [i for i in test_res.releases.keys() if i != 'latest']
    for version in test_res.releases:
        if version == 'latest':
            continue
        for _version in test_res.releases[version]:
            assert _version.file
            assert _version.file_url
            assert _version.md5
            assert _version.product_release_date
            assert _version.release_date
            assert _version.sha256
            assert _version.size
            assert _version.version
    for version in test_res.releases.latest:
        assert version in keys
        for _version in test_res.releases.latest[version]:
            assert _version.file
            assert _version.file_url
            assert _version.md5
            assert _version.product_release_date
            assert _version.release_date
            assert _version.sha256
            assert _version.size
            assert _version.version
    for item in test_res.signing_keys:
        assert item.file
        assert item.file_url
        assert item.md5
        assert item.sha256
        assert item.size


@responses.activate
def test_download():
    '''
    Test download method
    '''
    responses.add(
        method='GET',
        url=re.compile(r'https://www\.tenable\.com:443/downloads/api/v2/pages/.*/files/.*'),
        body=b'Line1\nLine2\nLine3\nLine4\nLine5\nLine6\nLine7\nLine8\nLine9',
        stream=True
    )
    dl = Downloads()

    # test returning a BytesIO object:
    fobj = dl.download('nessus', 'Nessus-latest-es7.x86_64.rpm')
    assert isinstance(fobj, BytesIO)

    # test using the context manager
    with BytesIO() as pkgfile:
        dl.download('nessus', 'Nessus-latest-es7.x86_64.rpm', pkgfile)
