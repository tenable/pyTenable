"""
DevianceApi
===========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`deviance <DevianceObject>` API endpoints.

Methods available on ``tad.deviance``:

.. rst-class:: hide-signature
.. autoclass:: DevianceApi

    .. automethod:: api_infrastructure_id_directory_id_deviances_get
    .. automethod:: api_infrastructure_id_directory_id_deviances_id_get
    .. automethod:: api_infrastructure_id_directory_id_deviances_id_patch
    .. automethod:: api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch
    .. automethod:: api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post
    .. automethod:: api_profiles_profile_id_checkers_checker_id_deviances_patch
    .. automethod:: api_profiles_profile_id_checkers_checker_id_deviances_post
    .. automethod:: api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get
    .. automethod:: api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post

"""
from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class DevianceApi(object):
    """
        Provide Security deviance items
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_infrastructure_id_directory_id_deviances_get(self, x_api_key, directory_id,
                                                                                     infrastructure_id, **kwargs):
        """Get all deviances for a directory.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_get(self,x_api_key, directory_id, infrastructure_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str page:
        :param str per_page:
        :param str batch_size:
        :param str last_identifier_seen:
        :param str resolved:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_deviances_get_with_http_info(
                self,x_api_key, directory_id, infrastructure_id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directory_id_deviances_get_with_http_info(
                self,x_api_key, directory_id, infrastructure_id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_deviances_get_with_http_info(self, x_api_key,
                                                                        directory_id,
                                                                        infrastructure_id,
                                                                        **kwargs):
        """Get all deviances for a directory.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_get_with_http_info(self,x_api_key, directory_id, infrastructure_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str directory_id: (required)
        :param str infrastructure_id: (required)
        :param str page:
        :param str per_page:
        :param str batch_size:
        :param str last_identifier_seen:
        :param str resolved:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'directory_id', 'infrastructure_id', 'page', 'per_page', 'batch_size',
                      'last_identifier_seen', 'resolved']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructure_id_directory_id_deviances_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructure_id_directory_id_deviances_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructure_id_directory_id_deviances_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructure_id_directory_id_deviances_get`")

        collection_formats = {}

        path_params = {}
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))
        if 'per_page' in params:
            query_params.append(('perPage', params['per_page']))
        if 'batch_size' in params:
            query_params.append(('batchSize', params['batch_size']))
        if 'last_identifier_seen' in params:
            query_params.append(('lastIdentifierSeen', params['last_identifier_seen']))
        if 'resolved' in params:
            query_params.append(('resolved', params['resolved']))

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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20019]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directory_id_deviances_id_get(self, x_api_key,
                                                            infrastructure_id, directory_id,
                                                            id, **kwargs):
        """Get ad-object-deviance-history instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_id_get(self,x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20020
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_deviances_id_get_with_http_info(self,
                x_api_key, infrastructure_id, directory_id, id, **kwargs)
        else:
            (
                data) = self.api_infrastructure_id_directory_id_deviances_id_get_with_http_info(self,
                x_api_key, infrastructure_id, directory_id, id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_deviances_id_get_with_http_info(self,
                                                                           x_api_key,
                                                                           infrastructure_id,
                                                                           directory_id, id,
                                                                           **kwargs):
        """Get ad-object-deviance-history instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_id_get_with_http_info(self,x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20020
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
                    " to method api_infrastructure_id_directory_id_deviances_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructure_id_directory_id_deviances_id_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructure_id_directory_id_deviances_id_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructure_id_directory_id_deviances_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructure_id_directory_id_deviances_id_get`")

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
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20020',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directory_id_deviances_id_patch(self, body, x_api_key,
                                                              infrastructure_id,directory_id, id, **kwargs):
        """Update ad-object-deviance-history instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_id_patch(self,body, x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeviancesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20020
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directory_id_deviances_id_patch_with_http_info(self,
                body, x_api_key, infrastructure_id, directory_id, id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directory_id_deviances_id_patch_with_http_info(self,
                body, x_api_key, infrastructure_id, directory_id, id, **kwargs)
            return data

    def api_infrastructure_id_directory_id_deviances_id_patch_with_http_info(self, body,x_api_key,
        infrastructure_id,directory_id,id, **kwargs):
        """Update ad-object-deviance-history instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directory_id_deviances_id_patch_with_http_info(self,body, x_api_key, infrastructure_id, directory_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeviancesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str id: (required)
        :return: InlineResponse20020
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'infrastructure_id', 'directory_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructure_id_directory_id_deviances_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_infrastructure_id_directory_id_deviances_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructure_id_directory_id_deviances_id_patch`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructure_id_directory_id_deviances_id_patch`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_infrastructure_id_directory_id_deviances_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructure_id_directory_id_deviances_id_patch`")

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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20020',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch(self, body, x_api_key,
                                                                                            profile_id, checker_id,
                                                                                            ad_object_id, **kwargs):
        """Update instances matching a checkerId and an AD object ID.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch(self,body, x_api_key, profile_id, checker_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdObjectIdDeviancesBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str ad_object_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch_with_http_info(
                body, x_api_key, profile_id, checker_id, ad_object_id, **kwargs)
        else:
            (
                data) = self.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch_with_http_info(
                body, x_api_key, profile_id, checker_id, ad_object_id, **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch_with_http_info(self, body,
                                                                                                           x_api_key,
                                                                                                           profile_id,
                                                                                                           checker_id,
                                                                                                           ad_object_id,
                                                                                                           **kwargs):
        """Update instances matching a checkerId and an AD object ID.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch_with_http_info(self,body, x_api_key, profile_id, checker_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdObjectIdDeviancesBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str ad_object_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'checker_id', 'ad_object_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch`")
            # verify the required parameter 'ad_object_id' is set
        if ('ad_object_id' not in params or
                params['ad_object_id'] is None):
            raise ValueError(
                "Missing the required parameter `ad_object_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']
        if 'ad_object_id' in params:
            path_params['adObjectId'] = params['ad_object_id']

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
            'api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{adObjectId}/deviances', 'PATCH',
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

    def api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post(self, body, x_api_key,
                                                                                           profile_id, checker_id,
                                                                                           ad_object_id, **kwargs):
        """Search all deviances by profile by checker by AD object   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post(self,body, x_api_key, profile_id, checker_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdObjectIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str ad_object_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post_with_http_info(self,
                body, x_api_key, profile_id, checker_id, ad_object_id, **kwargs)
        else:
            (
                data) = self.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post_with_http_info(self,
                body, x_api_key, profile_id, checker_id, ad_object_id, **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post_with_http_info(self, body,
                                                                                                          x_api_key,
                                                                                                          profile_id,
                                                                                                          checker_id,
                                                                                                          ad_object_id,
                                                                                                          **kwargs):
        """Search all deviances by profile by checker by AD object   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post_with_http_info(self,body, x_api_key, profile_id, checker_id, ad_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdObjectIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str ad_object_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'checker_id', 'ad_object_id', 'per_page', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post`")
            # verify the required parameter 'ad_object_id' is set
        if ('ad_object_id' not in params or
                params['ad_object_id'] is None):
            raise ValueError(
                "Missing the required parameter `ad_object_id` when calling `api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']
        if 'ad_object_id' in params:
            path_params['adObjectId'] = params['ad_object_id']

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
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{adObjectId}/deviances', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20019]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_checkers_checker_id_deviances_patch(self, body, x_api_key, profile_id, checker_id,
                                                                    **kwargs):
        """Update instances matching a checkerId.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_deviances_patch(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckerIdDeviancesBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_deviances_patch_with_http_info(self,body, x_api_key,
                                                                                                   profile_id,
                                                                                                   checker_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_checkers_checker_id_deviances_patch_with_http_info(self,body, x_api_key,
                                                                                                     profile_id,
                                                                                                     checker_id,
                                                                                                     **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_deviances_patch_with_http_info(self, body, x_api_key, profile_id,
                                                                                   checker_id, **kwargs):
        """Update instances matching a checkerId.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_deviances_patch_with_http_info(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckerIdDeviancesBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'checker_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_deviances_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_deviances_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_deviances_patch`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_deviances_patch`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_deviances_patch`")

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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/checkers/{checkerId}/deviances', 'PATCH',
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

    def api_profiles_profile_id_checkers_checker_id_deviances_post(self, body, x_api_key, profile_id, checker_id,
                                                                   **kwargs):
        """Get all deviances by checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_deviances_post(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckerIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :param str batch_size:
        :param str last_identifier_seen:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_deviances_post_with_http_info(self,body, x_api_key,
                                                                                                  profile_id,
                                                                                                  checker_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_checkers_checker_id_deviances_post_with_http_info(self,body, x_api_key,
                                                                                                    profile_id,
                                                                                                    checker_id,
                                                                                                    **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_deviances_post_with_http_info(self, body, x_api_key, profile_id,
                                                                                  checker_id, **kwargs):
        """Get all deviances by checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_deviances_post_with_http_info(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckerIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :param str batch_size:
        :param str last_identifier_seen:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'checker_id', 'per_page', 'page', 'batch_size',
                      'last_identifier_seen']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_deviances_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_deviances_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_deviances_post`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_deviances_post`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_deviances_post`")

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
        if 'batch_size' in params:
            query_params.append(('batchSize', params['batch_size']))
        if 'last_identifier_seen' in params:
            query_params.append(('lastIdentifierSeen', params['last_identifier_seen']))

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
            'api/profiles/{profileId}/checkers/{checkerId}/deviances', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20019]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get(
            self, x_api_key, profile_id, infrastructure_id, directory_id, checker_id, **kwargs):
        """Get all deviances related to a single directory and checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get(self,x_api_key, profile_id, infrastructure_id, directory_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get_with_http_info(
                self,x_api_key, profile_id, infrastructure_id, directory_id, checker_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get_with_http_info(
                self,x_api_key, profile_id, infrastructure_id, directory_id, checker_id, **kwargs)
            return data

    def api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get_with_http_info(
            self, x_api_key, profile_id, infrastructure_id, directory_id, checker_id, **kwargs):
        """Get all deviances related to a single directory and checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get_with_http_info(self,x_api_key, profile_id, infrastructure_id, directory_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str checker_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'infrastructure_id', 'directory_id', 'checker_id', 'per_page', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_checkers_checker_id_deviances_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']
        if 'directory_id' in params:
            path_params['directoryId'] = params['directory_id']
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
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/checkers/{checkerId}/deviances',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20019]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post(
            self, body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs):
        """Get all deviances by eventId.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post(self,body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EventIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post_with_http_info(
                self,body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs)
        else:
            (data) = self.api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post_with_http_info(
                self,body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs)
            return data

    def api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post_with_http_info(
            self, body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, **kwargs):
        """Get all deviances by eventId.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post_with_http_info(self,body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EventIdDeviancesBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str infrastructure_id: (required)
        :param str directory_id: (required)
        :param str event_id: (required)
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20019]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'profile_id', 'infrastructure_id', 'directory_id', 'event_id', 'per_page',
                      'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")
            # verify the required parameter 'directory_id' is set
        if ('directory_id' not in params or
                params['directory_id'] is None):
            raise ValueError(
                "Missing the required parameter `directory_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")
            # verify the required parameter 'event_id' is set
        if ('event_id' not in params or
                params['event_id'] is None):
            raise ValueError(
                "Missing the required parameter `event_id` when calling `api_profiles_profile_id_infrastructure_id_directory_id_events_event_id_deviances_post`")

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
            'api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/deviances',
            'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20019]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
