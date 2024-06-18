import datetime
import responses

from tenable.ie.deviance.api import DevianceIterator
from tests.ie.conftest import RE_BASE


@responses.activate
def test_deviance_list_with_batch_size(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/directories/1/deviances'
                  f'?batchSize=1&resolved=1&lastIdentifierSeen=1',
                  json=[{
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-07-30T00:59:12.000Z',
                      'id': 1,
                      'ignoreUntil': None,
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-08-23T07:30:41.000Z',
                      'resolvedEventId': 1
                  }]
                  )
    resp = api.deviance.list(
        infrastructure_id='1',
        directory_id='1',
        batch_size=1,
        resolved=True,
        last_identifier_seen=1
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['ad_object_id'] == 1
    assert resp[0]['attributes'][0]['name'] == 'attribute'
    assert resp[0]['attributes'][0]['value'] == 'test'
    assert resp[0]['checker_id'] == 1
    assert resp[0]['createdEventId'] == 1
    assert resp[0]['description']['replacements'][0]['name'] == 'attribute'
    assert resp[0]['description']['replacements'][0]['value_type'] == 'string'
    assert resp[0]['description']['template'] == 'template'
    assert resp[0]['deviance_provider_id'] == '1'
    assert resp[0]['directory_id'] == 1
    assert resp[0]['event_date'] == datetime.datetime(
        2021, 7, 30, 0, 59, 12, tzinfo=datetime.timezone.utc)
    assert resp[0]['id'] == 1
    assert resp[0]['ignore_until'] is None
    assert resp[0]['profile_id'] == 1
    assert resp[0]['reason_id'] == 1
    assert resp[0]['resolvedEventId'] == 1
    assert resp[0]['resolved_at'] == datetime.datetime(
        2021, 8, 23, 7, 30, 41, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_list_without_batch_size(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/directories/1/deviances'
                  f'?page=1&perPage=10&resolved=1&lastIdentifierSeen=1',
                  json=[{
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-07-30T00:59:12.000Z',
                      'id': 1,
                      'ignoreUntil': None,
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-08-23T07:30:41.000Z',
                      'resolvedEventId': 1
                  }]
                  )
    deviance = api.deviance.list(
        infrastructure_id='1',
        directory_id='1',
        page=1,
        per_page=10,
        resolved=True,
        last_identifier_seen=1
    )
    assert isinstance(deviance, DevianceIterator)
    resp = deviance.next()

    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2021, 7, 30, 0, 59, 12, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] is None
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] == 1
    assert resp['resolved_at'] == datetime.datetime(
        2021, 8, 23, 7, 30, 41, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_get_history_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/directories/1/deviances/1',
                  json={
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-08-18T03:44:34.000Z',
                      'id': 1,
                      'ignoreUntil': None,
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-09-17T06:28:27.000Z',
                      'resolvedEventId': 1
                  }
                  )
    resp = api.deviance.get_history_details(
        infrastructure_id='1',
        directory_id='1',
        deviance_id='1'
    )
    assert isinstance(resp, dict)
    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2021, 8, 18, 3, 44, 34, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] is None
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] == 1
    assert resp['resolved_at'] == datetime.datetime(
        2021, 9, 17, 6, 28, 27, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_update_history_details(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/infrastructures/1/directories/1/deviances/1',
                  json={
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-08-18T03:44:34.000Z',
                      'id': 1,
                      'ignoreUntil': '2022-01-27T23:59:59.999Z',
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-09-17T06:28:27.000Z',
                      'resolvedEventId': 1
                  }
                  )
    resp = api.deviance.update_history_details(
        directory_id='1',
        infrastructure_id='1',
        deviance_id='1',
        ignore_until='2022-01-27T23:59:59.999Z'
    )
    assert isinstance(resp, dict)
    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2021, 8, 18, 3, 44, 34, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] == datetime.datetime(
        2022, 1, 27, 23, 59, 59, 999000, tzinfo=datetime.timezone.utc)
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] == 1
    assert resp['resolved_at'] == datetime.datetime(
        2021, 9, 17, 6, 28, 27, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_list_by_directory_and_checker(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/infrastructures/1/'
                  f'directories/1/checkers/1/deviances?perPage=10&page=1',
                  json=[{
                      'ad_object_id': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checker_id': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'value_type': 'string'
                          }],
                          'template': 'template'
                      },
                      'deviance_provider_id': '1',
                      'directory_id': 1,
                      'event_date': '2022-01-25T05:40:01.000Z',
                      'id': 1,
                      'ignore_until': None,
                      'profile_id': 1,
                      'reason_id': 1,
                      'resolvedEventId': None,
                      'resolved_at': None
                  }]
                  )
    deviance = api.deviance.list_by_directory_and_checker(
        infrastructure_id='1',
        directory_id='1',
        profile_id='1',
        checker_id='1',
        page=1,
        per_page=10
    )
    assert isinstance(deviance, DevianceIterator)
    resp = deviance.next()

    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2022, 1, 25, 5, 40, 1, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] is None
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] is None
    assert resp['resolved_at'] is None


@responses.activate
def test_deviance_list_by_checker_with_batch_size(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/checkers/1/deviances'
                  f'?lastIdentifierSeen=1&batchSize=1',
                  json=[{
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-07-30T00:59:12.000Z',
                      'id': 1,
                      'ignoreUntil': None,
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-08-23T07:30:41.000Z',
                      'resolvedEventId': 1
                  }]
                  )
    resp = api.deviance.list_by_checker(
        profile_id='1',
        checker_id='1',
        expression={'OR': [{'whencreated': '2021-07-29T12:27:50.0000000Z'}]},
        batch_size=1,
        last_identifier_seen=1
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['ad_object_id'] == 1
    assert resp[0]['attributes'][0]['name'] == 'attribute'
    assert resp[0]['attributes'][0]['value'] == 'test'
    assert resp[0]['checker_id'] == 1
    assert resp[0]['createdEventId'] == 1
    assert resp[0]['description']['replacements'][0]['name'] == 'attribute'
    assert resp[0]['description']['replacements'][0]['value_type'] == 'string'
    assert resp[0]['description']['template'] == 'template'
    assert resp[0]['deviance_provider_id'] == '1'
    assert resp[0]['directory_id'] == 1
    assert resp[0]['event_date'] == datetime.datetime(
        2021, 7, 30, 0, 59, 12, tzinfo=datetime.timezone.utc)
    assert resp[0]['id'] == 1
    assert resp[0]['ignore_until'] is None
    assert resp[0]['profile_id'] == 1
    assert resp[0]['reason_id'] == 1
    assert resp[0]['resolvedEventId'] == 1
    assert resp[0]['resolved_at'] == datetime.datetime(
        2021, 8, 23, 7, 30, 41, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_list_by_checker_without_batch_size(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/checkers/1/deviances'
                  f'?page=1&perPage=10&lastIdentifierSeen=1',
                  json=[{
                      'adObjectId': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checkerId': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      },
                      'devianceProviderId': '1',
                      'directoryId': 1,
                      'eventDate': '2021-07-30T00:59:12.000Z',
                      'id': 1,
                      'ignoreUntil': None,
                      'profileId': 1,
                      'reasonId': 1,
                      'resolvedAt': '2021-08-23T07:30:41.000Z',
                      'resolvedEventId': 1
                  }]
                  )
    deviance = api.deviance.list_by_checker(
        profile_id='1',
        checker_id='1',
        expression={'OR': [{'whencreated': '2021-07-29T12:27:50.0000000Z'}]},
        page=1,
        per_page=10,
        last_identifier_seen=1
    )
    assert isinstance(deviance, DevianceIterator)
    resp = deviance.next()

    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2021, 7, 30, 0, 59, 12, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] is None
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] == 1
    assert resp['resolved_at'] == datetime.datetime(
        2021, 8, 23, 7, 30, 41, tzinfo=datetime.timezone.utc)


@responses.activate
def test_deviance_update_by_checker(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/profiles/1/checkers/1/deviances',
                  json=None
                  )
    resp = api.deviance.update_by_checker(
        profile_id='1',
        checker_id='1',
        ignore_until='2022-01-27T23:59:59.999Z'
    )
    assert resp is None


@responses.activate
def test_deviance_search(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/checkers/1/'
                  f'ad-objects/1/deviances?perPage=10&page=1',
                  json=[{
                      'ad_object_id': 1,
                      'attributes': [{
                          'name': 'attribute',
                          'value': 'test'
                      }],
                      'checker_id': 1,
                      'createdEventId': 1,
                      'description': {
                          'replacements': [{
                              'name': 'attribute',
                              'value_type': 'string'
                          }],
                          'template': 'template'
                      },
                      'deviance_provider_id': '1',
                      'directory_id': 1,
                      'event_date': '2022-01-25T05:40:01.000Z',
                      'id': 1,
                      'ignore_until': None,
                      'profile_id': 1,
                      'reason_id': 1,
                      'resolvedEventId': None,
                      'resolved_at': None
                  }]
                  )
    deviance = api.deviance.search(
        profile_id=1,
        checker_id=1,
        ad_object_id=1,
        show_ignored=False,
        page=1,
        per_page=10
    )
    assert isinstance(deviance, DevianceIterator)
    resp = deviance.next()

    assert resp['ad_object_id'] == 1
    assert resp['attributes'][0]['name'] == 'attribute'
    assert resp['attributes'][0]['value'] == 'test'
    assert resp['checker_id'] == 1
    assert resp['createdEventId'] == 1
    assert resp['description']['replacements'][0]['name'] == 'attribute'
    assert resp['description']['replacements'][0]['value_type'] == 'string'
    assert resp['description']['template'] == 'template'
    assert resp['deviance_provider_id'] == '1'
    assert resp['directory_id'] == 1
    assert resp['event_date'] == datetime.datetime(
        2022, 1, 25, 5, 40, 1, tzinfo=datetime.timezone.utc)
    assert resp['id'] == 1
    assert resp['ignore_until'] is None
    assert resp['profile_id'] == 1
    assert resp['reason_id'] == 1
    assert resp['resolvedEventId'] is None
    assert resp['resolved_at'] is None


@responses.activate
def test_deviance_update_on_ado_and_checker(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/profiles/1/checkers/1/ad-objects/1/deviances',
                  json=None
                  )
    resp = api.deviance.update_on_ado_and_checker(
        profile_id='1',
        checker_id='1',
        ad_object_id='1',
        ignore_until='2022-01-27T23:59:59.999Z'
    )
    assert resp is None
