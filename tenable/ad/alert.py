# coding: utf-8
"""
AlertAPI
===========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`alert <AlertObject>` API endpoints.

Methods available on ``tad.alert``:

.. rst-class:: hide-signature
.. autoclass:: AlertApi

    .. automethod:: api_alerts_id_get
    .. automethod:: api_alerts_id_patch
    .. automethod:: api_profiles_profile_id_alerts_get
    .. automethod:: api_profiles_profile_id_alerts_patch

"""

from __future__ import absolute_import
import six

from tenable.ad.api_client import ApiClient


class AlertApi(object):
    """
        Provide the New deviances alert
    """
    api_client = ApiClient()
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_alerts_id_get(self, x_api_key, id, **kwargs):
        """Get alert instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_alerts_id_get(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_alerts_id_get_with_http_info(self,x_api_key, id, **kwargs)
        else:
            (data) = self.api_alerts_id_get_with_http_info(self,x_api_key, id, **kwargs)
            return data

    def api_alerts_id_get_with_http_info(self, x_api_key, id, **kwargs):
        """Get alert instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_alerts_id_get_with_http_info(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_alerts_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_alerts_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_alerts_id_get`")

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

        header_params = {}
        if 'x_api_key' in params:
            header_params['x-api-key'] = params['x_api_key']

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/alerts/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2005',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_alerts_id_patch(self, body, x_api_key, id, **kwargs):
        """Update alert instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_alerts_id_patch(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AlertsIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_alerts_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
        else:
            (data) = self.api_alerts_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
            return data

    def api_alerts_id_patch_with_http_info(self, body, x_api_key, id, **kwargs):
        """Update alert instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_alerts_id_patch_with_http_info(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AlertsIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_alerts_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_alerts_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_alerts_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_alerts_id_patch`")

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

        header_params = {}
        if 'x_api_key' in params:
            header_params['x-api-key'] = params['x_api_key']

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/alerts/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2005',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_alerts_get(self, x_api_key, profile_id, **kwargs):
        """Retrieve all alert instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_alerts_get(self,x_api_key, profile_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str archived:
        :param str read:
        :param str per_page:
        :param str page:
        :return: list[InlineResponse2005]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_alerts_get_with_http_info(self,x_api_key, profile_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_alerts_get_with_http_info(self,x_api_key, profile_id, **kwargs)
            return data

    def api_profiles_profile_id_alerts_get_with_http_info(self, x_api_key, profile_id, **kwargs):
        """Retrieve all alert instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_alerts_get_with_http_info(self,x_api_key, profile_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str archived:
        :param str read:
        :param str per_page:
        :param str page:
        :return: list[InlineResponse2005]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'archived', 'read', 'per_page', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_alerts_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_alerts_get`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_alerts_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']

        query_params = []
        if 'archived' in params:
            query_params.append(('archived', params['archived']))
        if 'read' in params:
            query_params.append(('read', params['read']))
        if 'per_page' in params:
            query_params.append(('perPage', params['per_page']))
        if 'page' in params:
            query_params.append(('page', params['page']))

        header_params = {}
        if 'x_api_key' in params:
            header_params['x-api-key'] = params['x_api_key']

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/alerts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse2005]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_alerts_patch(self, body, x_api_key, profile_id, **kwargs):
        """Update alerts for one profile   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_alerts_patch(self,body, x_api_key, profile_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ProfileIdAlertsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_alerts_patch_with_http_info(self,body, x_api_key, profile_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_alerts_patch_with_http_info(self,body, x_api_key, profile_id, **kwargs)
            return data

    def api_profiles_profile_id_alerts_patch_with_http_info(self, body, x_api_key, profile_id, **kwargs):
        """Update alerts for one profile   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_alerts_patch_with_http_info(self,body, x_api_key, profile_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ProfileIdAlertsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_alerts_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_alerts_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_alerts_patch`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_alerts_patch`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']

        query_params = []

        header_params = {}
        if 'x_api_key' in params:
            header_params['x-api-key'] = params['x_api_key']

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/alerts', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Object',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
