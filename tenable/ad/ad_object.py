# coding: utf-8

"""
ADObjectAPI
===========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`ad-object <ADObject>` API endpoints.

Methods available on ``tad.ad_object``:

.. rst-class:: hide-signature
.. autoclass:: ADObjectApi

    .. automethod:: api_infrastructure_id_directory_id_ad_objects_id_get
    .. automethod:: api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get
    .. automethod:: api_infrastructure_id_directory_id_event_id_ad_objects_id_get
    .. automethod:: api_profile_id_checker_id_ad_objects_id_get
    .. automethod:: api_profile_id_checker_id_ad_objects_search_post


"""
from __future__ import absolute_import
import six
from tenable.ad.api_client import ApiClient as api, ApiClient


class ADObjectApi(object):
    """
        This is for generating rest calls on the ADObjectApi
        Provide Representation of an Active Directory Object
    """
    api_client = ApiClient()
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_infrastructure_id_directory_id_ad_objects_id_get(self, x_api_key, directory_id,
                                                            infrastructure_id, id,**kwargs):
        """Get ad-object instance by id.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_ad_objects_id_get(self,x_api_key, directory_id, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_ad_objects_id_get_with_http_info(self,
                x_api_key, directory_id, infrastructure_id, id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directory_id_ad_objects_id_get_with_http_info(self,
                x_api_key, directory_id, infrastructure_id, id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_ad_objects_id_get_with_http_info(self, x_api_key,
        directory_id,infrastructure_id,id, **kwargs):
        """Get ad-object instance by id.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_ad_objects_id_get_with_http_info(self,x_api_key, directory_id, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'directory_id', 'infrastructure_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get`")
        # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get`")
        # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get`")
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get`")

        collection_formats = {}

        path_params = {}
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/ad-objects/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2001',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get(self,x_api_key,
         infrastructure_id,
         directory_id,
         event_id,
         id,
         **kwargs):
        """Get one ad-object changes between a given event and the event which precedes it

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get(self,x_api_key, infrastructure_id, directory_id, event_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :param str id: (required)
        :param list[str] wanted_values:
        :param str event_provider_id:
        :return: list[InlineResponse2003]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get_with_http_info(self,
                x_api_key, infrastructure_id, directory_id, event_id, id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get_with_http_info(self,
                x_api_key, infrastructure_id, directory_id, event_id, id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get_with_http_info(
            self, x_api_key, infrastructure_id, directory_id, event_id, id, **kwargs):
        """Get one ad-object changes between a given event and the event which precedes it

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get_with_http_info(self,x_api_key, infrastructure_id, directory_id, event_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :param str id: (required)
        :param list[str] wanted_values:
        :param str event_provider_id:
        :return: list[InlineResponse2003]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id', 'directory_id', 'event_id', 'id', 'wanted_values',
                      'event_provider_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get`")
        # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get`")
        # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get`")
        # verify the required parameter 'event_id' is set
        if ('event_id' not in params or
                params['event_id'] is None):
            raise ValueError(
                "Missing the required parameter `event_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get`")
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get`")

        collection_formats = {}

        path_params = {}
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'event_id' in params:
            path_params['eventId'] = params['event_id']
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []
        if 'wanted_values' in params:
            query_params.append(('wantedValues', params['wanted_values']))
            collection_formats['wantedValues'] = 'multi'
        if 'event_provider_id' in params:
            query_params.append(('eventProviderId', params['event_provider_id']))

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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/ad-objects/{id}/changes',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse2003]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directory_id_event_id_ad_objects_id_get(self,
        x_api_key,
        directory_id,
        infrastructure_id,
        id, event_id,
        **kwargs):
        """Get ad-object instance by id.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_event_id_ad_objects_id_get(self,x_api_key, directory_id, infrastructure_id, id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :param str event_id: (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_event_id_ad_objects_id_get_with_http_info(self,
                x_api_key, directory_id, infrastructure_id, id, event_id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directory_id_event_id_ad_objects_id_get_with_http_info(self,
                x_api_key, directory_id, infrastructure_id, id, event_id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_event_id_ad_objects_id_get_with_http_info(
            self, x_api_key, directory_id, infrastructure_id, id, event_id, **kwargs):
        """Get ad-object instance by id.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_event_id_ad_objects_id_get_with_http_info(self,x_api_key, directory_id, infrastructure_id, id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :param str event_id: (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'directory_id', 'infrastructure_id', 'id', 'event_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get`")
        # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get`")
        # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get`")
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get`")
        # verify the required parameter 'event_id' is set
        if ('event_id' not in params or
                params['event_id'] is None):
            raise ValueError(
                "Missing the required parameter `event_id` when calling `api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get`")

        collection_formats = {}

        path_params = {}
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'id' in params:
            path_params['id'] = params['id']
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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/ad-objects/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2001',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profile_id_checker_id_ad_objects_id_get(self, x_api_key, profile_id, checker_id, id,
                                                                      **kwargs):
        """Retrieve an AD object by id that have deviances for a specific profile and checker

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profile_id_checker_id_ad_objects_id_get(self,x_api_key, profile_id, checker_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str id: (required)
        :param str show_ignored:
        :return: InlineResponse2002
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profile_id_checker_id_ad_objects_id_get_with_http_info(self,x_api_key,
                                                                                                     profile_id,
                                                                                                     checker_id, id,
                                                                                                     **kwargs)
        else:
            (data) = self.api_profile_id_checker_id_ad_objects_id_get_with_http_info(self,x_api_key,
                                                                                                       profile_id,
                                                                                                       checker_id, id,
                                                                                                       **kwargs)
            return data

    def api_profile_id_checker_id_ad_objects_id_get_with_http_info(self, x_api_key, profile_id,
                                                                                     checker_id, id, **kwargs):
        """Retrieve an AD object by id that have deviances for a specific profile and checker

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profile_id_checker_id_ad_objects_id_get_with_http_info(self,x_api_key, profile_id, checker_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str id: (required)
        :param str show_ignored:
        :return: InlineResponse2002
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'checker_id', 'id', 'show_ignored']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_ad_objects_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_id_get`")
        # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_id_get`")
        # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_id_get`")
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_id_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []
        if 'show_ignored' in params:
            query_params.append(('showIgnored', params['show_ignored']))

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
            'api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2002',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profile_id_checker_id_ad_objects_search_post(self, body, x_api_key, profile_id,
                                                                           checker_id, **kwargs):
        """Search all AD objects having deviances by profile by checker

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profile_id_checker_id_ad_objects_search_post(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdobjectsSearchBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse2004]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            (data) = self.api_profile_id_checker_id_ad_objects_search_post_with_http_info(self,body,
            x_api_key,
            profile_id,
            checker_id,
            **kwargs)
        else:
            (data) = self.api_profile_id_checker_id_ad_objects_search_post_with_http_info(self,body,
            x_api_key,
            profile_id,
            checker_id,
            **kwargs)
        return data

    def api_profile_id_checker_id_ad_objects_search_post_with_http_info(self, body, x_api_key,
                                                                                          profile_id, checker_id,
                                                                                          **kwargs):
        """Search all AD objects having deviances by profile by checker

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profile_id_checker_id_ad_objects_search_post_with_http_info(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdobjectsSearchBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse2004]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'checker_id', 'per_page', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_ad_objects_search_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_search_post`")
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_search_post`")
        # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_search_post`")
        # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_search_post`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']

        query_params = []
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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/checkers/{checkerId}/ad-objects/search', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse2004]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
