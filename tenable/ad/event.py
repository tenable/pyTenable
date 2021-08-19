"""
EventApi
=============

The following methods allow for interaction into the Tenable.ad
:tenableAD:`event <EventObject>` API endpoints.

Methods available on ``tad.reason``:

.. rst-class:: hide-signature
.. autoclass:: EventApi

    .. automethod:: api_events_event_provider_id_last_events_get
    .. automethod:: api_events_last_get
    .. automethod:: api_events_search_post
    .. automethod:: api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get
    .. automethod:: api_infrastructures_infrastructure_id_directories_directory_id_events_id_get

"""

from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class EventApi(object):
    """
        Provide a change in the Active Directory
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_events_event_provider_id_last_events_get(self, x_api_key, event_provider_id, **kwargs):
        """Get the last events for each AD object source and directory   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_event_provider_id_last_events_get(self,x_api_key, event_provider_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str event_provider_id: (required)
        :return: list[InlineResponse20025]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_events_event_provider_id_last_events_get_with_http_info(self,x_api_key, event_provider_id,
                                                                                    **kwargs)
        else:
            (data) = self.api_events_event_provider_id_last_events_get_with_http_info(self,x_api_key, event_provider_id,
                                                                                      **kwargs)
            return data

    def api_events_event_provider_id_last_events_get_with_http_info(self, x_api_key, event_provider_id, **kwargs):
        """Get the last events for each AD object source and directory   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_event_provider_id_last_events_get_with_http_info(self,x_api_key, event_provider_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str event_provider_id: (required)
        :return: list[InlineResponse20025]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'event_provider_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_events_event_provider_id_last_events_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_events_event_provider_id_last_events_get`")
            # verify the required parameter 'event_provider_id' is set
        if ('event_provider_id' not in params or
                params['event_provider_id'] is None):
            raise ValueError(
                "Missing the required parameter `event_provider_id` when calling `api_events_event_provider_id_last_events_get`")

        collection_formats = {}

        path_params = {}
        if 'event_provider_id' in params:
            path_params['eventProviderId'] = params['event_provider_id']

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
            'api/events/{eventProviderId}/last-events', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20025]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_events_last_get(self, x_api_key, **kwargs):
        """Get the last event   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_last_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_events_last_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_events_last_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_events_last_get_with_http_info(self, x_api_key, **kwargs):
        """Get the last event   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_last_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_events_last_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_events_last_get`")

        collection_formats = {}

        path_params = {}

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
            'api/events/last', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20024',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_events_search_post(self, body, x_api_key, **kwargs):
        """Search events instances   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_search_post(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EventsSearchBody body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20024]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_events_search_post_with_http_info(self,body, x_api_key, **kwargs)
        else:
            (data) = self.api_events_search_post_with_http_info(self,body, x_api_key, **kwargs)
            return data

    def api_events_search_post_with_http_info(self, body, x_api_key, **kwargs):
        """Search events instances   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_events_search_post_with_http_info(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EventsSearchBody body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20024]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_events_search_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_events_search_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_events_search_post`")

        collection_formats = {}

        path_params = {}

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
            'api/events/search', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20024]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(self,
                                                                                                               x_api_key,
                                                                                                               infrastructure_id,
                                                                                                               directory_id,
                                                                                                               ad_object_id,
                                                                                                               **kwargs):
        """Get the last event related to an AD Object   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(self,x_api_key, infrastructure_id, directory_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str ad_object_id: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get_with_http_info(
                self,x_api_key, infrastructure_id, directory_id, ad_object_id, **kwargs)
        else:
            (
                data) = self.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get_with_http_info(
                self,x_api_key, infrastructure_id, directory_id, ad_object_id, **kwargs)
            return data

    def api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get_with_http_info(
            self, x_api_key, infrastructure_id, directory_id, ad_object_id, **kwargs):
        """Get the last event related to an AD Object   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get_with_http_info(self,x_api_key, infrastructure_id, directory_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str ad_object_id: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id', 'directory_id', 'ad_object_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get`")
            # verify the required parameter 'ad_object_id' is set
        if ('ad_object_id' not in params or
                params['ad_object_id'] is None):
            raise ValueError(
                "Missing the required parameter `ad_object_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get`")

        collection_formats = {}

        path_params = {}
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'ad_object_id' in params:
            path_params['adObjectId'] = params['ad_object_id']

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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/ad-objects/{adObjectId}/events/last',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20024',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(self, x_api_key, infrastructure_id,
                                                                                     directory_id, id, **kwargs):
        """Get event instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(self,x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get_with_http_info(
                self,x_api_key, infrastructure_id, directory_id, id, **kwargs)
        else:
            (data) = self.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get_with_http_info(
                self,x_api_key, infrastructure_id, directory_id, id, **kwargs)
            return data

    def api_infrastructures_infrastructure_id_directories_directory_id_events_id_get_with_http_info(self, x_api_key,
                                                                                                    infrastructure_id,
                                                                                                    directory_id, id,
                                                                                                    **kwargs):
        """Get event instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get_with_http_info(self,x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id', 'directory_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_directory_id_events_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_id_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_id_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_id_get`")

        collection_formats = {}

        path_params = {}
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20024',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
