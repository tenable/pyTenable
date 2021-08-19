"""
ReasonApi
=============

The following methods allow for interaction into the Tenable.ad
:tenableAD:`reason <ReasonObject>` API endpoints.

Methods available on ``tad.reason``:

.. rst-class:: hide-signature
.. autoclass:: ReasonApi

    .. automethod:: api_profiles_profile_id_checkers_checker_id_reasons_get
    .. automethod:: api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get
    .. automethod:: api_reasons_get
    .. automethod:: api_reasons_id_get

"""

from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class ReasonApi(object):
    """
        Provide the reason why a AD object is marked as deviant
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_profiles_profile_id_checkers_checker_id_reasons_get(self, x_api_key, profile_id, checker_id, **kwargs):
        """Retrieve all reason instances that have deviances for a specific profile and checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_reasons_get(self,x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: list[InlineResponse20032]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_reasons_get_with_http_info(self,x_api_key, profile_id,
                                                                                               checker_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_checkers_checker_id_reasons_get_with_http_info(self,x_api_key, profile_id,
                                                                                                 checker_id, **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_reasons_get_with_http_info(self, x_api_key, profile_id, checker_id,
                                                                               **kwargs):
        """Retrieve all reason instances that have deviances for a specific profile and checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_reasons_get_with_http_info(self,x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: list[InlineResponse20032]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'checker_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_reasons_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_reasons_get`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_reasons_get`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_reasons_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']

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
            'api/profiles/{profileId}/checkers/{checkerId}/reasons', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20032]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get(
            self, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs):
        """Retrieve all reason instances for which we have deviances for a specific profile, directory and event.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get(self,x_api_key, profile_id, infrastructure_id, directory_id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :return: list[InlineResponse20032]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get_with_http_info(
                self,x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get_with_http_info(
                self,x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs)
            return data

    def api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get_with_http_info(
            self, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs):
        """Retrieve all reason instances for which we have deviances for a specific profile, directory and event.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get_with_http_info(self,x_api_key, profile_id, infrastructure_id, directory_id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :return: list[InlineResponse20032]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'infrastructure_id', 'directory_id', 'event_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get`")
            # verify the required parameter 'event_id' is set
        if ('event_id' not in params or
                params['event_id'] is None):
            raise ValueError(
                "Missing the required parameter `event_id` when calling `api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'event_id' in params:
            path_params['eventId'] = params['event_id']

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
            'api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/reasons',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20032]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_reasons_get(self, x_api_key, **kwargs):
        """Retrieve all reason instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_reasons_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20032]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_reasons_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_reasons_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_reasons_get_with_http_info(self, x_api_key, **kwargs):
        """Retrieve all reason instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_reasons_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20032]
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
                    " to method api_reasons_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_reasons_get`")

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
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/reasons', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20032]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_reasons_id_get(self, x_api_key, id, **kwargs):
        """Get reason instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_reasons_id_get(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20032
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_reasons_id_get_with_http_info(self,x_api_key, id, **kwargs)
        else:
            (data) = self.api_reasons_id_get_with_http_info(self,x_api_key, id, **kwargs)
            return data

    def api_reasons_id_get_with_http_info(self, x_api_key, id, **kwargs):
        """Get reason instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_reasons_id_get_with_http_info(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20032
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
                    " to method api_reasons_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_reasons_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_reasons_id_get`")

        collection_formats = {}

        path_params = {}
        url = 'api/reasons/' + str(id)
        #if 'id' in params:
        #    path_params['id'] = params['id']

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
            url, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20032',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
