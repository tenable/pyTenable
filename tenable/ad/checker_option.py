# coding: utf-8

"""
CheckerOptionApi
========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`checker-options <CheckerOptionApi>` API endpoints.

Methods available on ``tad.checker_option``:

.. rst-class:: hide-signature
.. autoclass:: CheckerOptionApi

    .. automethod:: api_profiles_profile_id_checkers_checker_id_checker_options_get
    .. automethod:: api_profiles_profile_id_checkers_checker_id_checker_options_post

"""
from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class CheckerOptionApi(object):
    """
        Provide Checker options, configured for a directory, a checker and a profile
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_profiles_profile_id_checkers_checker_id_checker_options_get(self, x_api_key, profile_id, checker_id,
                                                                        **kwargs):
        """Get all checker options related to a checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_get(self,x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str staged:
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20017]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_checker_options_get_with_http_info(self,x_api_key,
                                                                                                       profile_id,
                                                                                                       checker_id,
                                                                                                       **kwargs)
        else:
            (data) = self.api_profiles_profile_id_checkers_checker_id_checker_options_get_with_http_info(self,x_api_key,
                                                                                                         profile_id,
                                                                                                         checker_id,
                                                                                                         **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_checker_options_get_with_http_info(self, x_api_key, profile_id,
                                                                                       checker_id, **kwargs):
        """Get all checker options related to a checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_get_with_http_info(self,x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :param str staged:
        :param str per_page:
        :param str page:
        :return: list[InlineResponse20017]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'profile_id', 'checker_id', 'staged', 'per_page', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_profiles_profile_id_checkers_checker_id_checker_options_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_get`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_get`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_get`")

        collection_formats = {}

        path_params = {}
        if 'profile_id' in params:
            path_params['profileId'] = params['profile_id']
        if 'checker_id' in params:
            path_params['checkerId'] = params['checker_id']

        query_params = []
        if 'staged' in params:
            query_params.append(('staged', params['staged']))
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
            'api/profiles/{profileId}/checkers/{checkerId}/checker-options', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20017]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_profiles_profile_id_checkers_checker_id_checker_options_post(self, body, x_api_key, profile_id, checker_id,
                                                                         **kwargs):
        """Create checker options related to a checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_post(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[CheckerIdCheckeroptionsBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: list[InlineResponse20017]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_profiles_profile_id_checkers_checker_id_checker_options_post_with_http_info(self,body, x_api_key,
                                                                                                        profile_id,
                                                                                                        checker_id,
                                                                                                        **kwargs)
        else:
            (data) = self.api_profiles_profile_id_checkers_checker_id_checker_options_post_with_http_info(self,body,
                                                                                                          x_api_key,
                                                                                                          profile_id,
                                                                                                          checker_id,
                                                                                                          **kwargs)
            return data

    def api_profiles_profile_id_checkers_checker_id_checker_options_post_with_http_info(self, body, x_api_key,
                                                                                        profile_id, checker_id,
                                                                                        **kwargs):
        """Create checker options related to a checker.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_post_with_http_info(self,body, x_api_key, profile_id, checker_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[CheckerIdCheckeroptionsBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :param str profile_id: (required)
        :param str checker_id: (required)
        :return: list[InlineResponse20017]
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
                    " to method api_profiles_profile_id_checkers_checker_id_checker_options_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_post`")
            # verify the required parameter 'profile_id' is set
        if ('profile_id' not in params or
                params['profile_id'] is None):
            raise ValueError(
                "Missing the required parameter `profile_id` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_post`")
            # verify the required parameter 'checker_id' is set
        if ('checker_id' not in params or
                params['checker_id'] is None):
            raise ValueError(
                "Missing the required parameter `checker_id` when calling `api_profiles_profile_id_checkers_checker_id_checker_options_post`")

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
            'api/profiles/{profileId}/checkers/{checkerId}/checker-options', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20017]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
