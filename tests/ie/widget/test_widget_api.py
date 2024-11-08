import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_widgets_list(api):
    '''
    tests the widget list api.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/dashboards/1/widgets',
                  json=[
                      {'dashboard_id': 1,
                       'height': 22,
                       'id': 1,
                       'pos_x': 11,
                       'pos_y': 12,
                       'title': 'test_widget',
                       'width': 21}
                  ]
                  )
    resp = api.widgets.list(dashboard_id='1')
    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
def test_widgets_create(api):
    '''
    tests the widget create api.
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/dashboards/1/widgets',
                  json={'dashboardId': '1',
                        'height': 22,
                        'id': 1,
                        'posX': 11,
                        'posY': 12,
                        'title': 'test_widget',
                        'width': 21
                        }
                  )
    resp = api.widgets.create(dashboard_id='1',
                              pos_x=11,
                              pos_y=12,
                              width=21,
                              height=22,
                              title='test_widget'
                              )
    assert isinstance(resp, dict)
    assert resp['title'] == 'test_widget'
    assert resp['pos_x'] == 11
    assert resp['pos_y'] == 12
    assert resp['width'] == 21
    assert resp['height'] == 22


@responses.activate
def test_widgets_update(api):
    '''
    tests the widget update api.
    '''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/dashboards/1/widgets/1',
                  json={'dashboardId': '1',
                        'height': 22,
                        'id': 1,
                        'posX': 11,
                        'posY': 12,
                        'title': 'EDITED',
                        'width': 21
                        }
                  )
    resp = api.widgets.update(dashboard_id='1',
                              widget_id=1,
                              name='EDITED'
                              )
    assert isinstance(resp, dict)
    assert resp['title'] == 'EDITED'
    assert resp['pos_x'] == 11
    assert resp['pos_y'] == 12
    assert resp['width'] == 21
    assert resp['height'] == 22


@responses.activate
def test_widgets_details(api):
    '''
    tests the widget details api.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/dashboards/1/widgets/1',
                  json={'dashboardId': '1',
                        'height': 22,
                        'id': 1,
                        'posX': 11,
                        'posY': 12,
                        'title': 'test_widget',
                        'width': 21
                        }
                  )
    resp = api.widgets.details(dashboard_id='1',
                               widget_id=1
                               )
    assert isinstance(resp, dict)
    assert resp['title'] == 'test_widget'
    assert resp['pos_x'] == 11
    assert resp['pos_y'] == 12
    assert resp['width'] == 21
    assert resp['height'] == 22


@responses.activate
def test_widgets_widget_options_details(api):
    '''
    tests the widget options details api.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/dashboards/1/widgets/1/options',
                  json={'type': 'BigNumber',
                        'series': [
                            {
                                'dataOptions': {
                                    'duration': 10,
                                    'interval': '10',
                                    'directoryIds': [1, 2, 3],
                                    'active': True
                                },
                                'displayOptions': {
                                    'label': 'User'
                                }
                            }
                        ]
                        }
                  )
    resp = api.widgets.widget_options_details(dashboard_id='1',
                                              widget_id=1
                                              )
    assert isinstance(resp, dict)
    assert resp['type'] == 'BigNumber'
    for s in resp['series']:
        assert s['data_options']['duration'] == 10
        assert s['data_options']['interval'] == '10'
        assert s['data_options']['directory_ids'] == [1, 2, 3]
        assert s['data_options']['active'] is True
        assert s['display_options']['label'] == 'User'


@responses.activate
def test_widget_delete(api):
    '''
    tests the  widget delete instance api.
    '''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/dashboards/1/widgets/1',
                  json=None

                  )
    resp = api.widgets.delete(dashboard_id=1, widget_id=1)
    assert resp is None


@responses.activate
def test_widget_define_widget_options(api):
    '''
    tests the define widget option api.
    '''
    responses.add(responses.PUT,
                  f'{RE_BASE}/dashboards/13/widgets/60/options',
                  json={
                      'type': 'BigNumber',
                      'series': [
                          {
                              'dataOptions': {
                                  'duration': 10,
                                  'interval': '10',
                                  'directoryIds': [1, 2, 3],
                                  'active': True
                              },
                              'displayOptions': {
                                  'label': 'User'
                              }
                          }
                      ]
                  }
                  )
    resp = api.widgets.define_widget_options(
        dashboard_id=13,
        widget_id=60,
        chart_type='BigNumber',
        series=[
            {
                'dataOptions': {
                    'type': 'User',
                    'duration': 1,
                    'directoryIds': [1, 2, 3],
                    'active': True
                },
                'displayOptions': {
                    'label': 'label'
                }
            }
        ]
    )
    assert resp is None
