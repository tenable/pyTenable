"""
AttackApi
=========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`attack <AttackApi>` API endpoints.

Methods available on ``tad.attack``:

.. rst-class:: hide-signature
.. autoclass:: AttackApi

    .. automethod:: api_attack_settings_gpo_get
    .. automethod:: api_attack_types_get
    .. automethod:: api_attacks_get
    .. automethod:: api_attacks_id_patch
    .. automethod:: api_attacks_post

"""

from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class AttackApi(object):
    """
        Provide Attacks as detected by Tenable.ad
    """
    api_client = ApiClient()
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_attack_settings_gpo_get(self, x_api_key, **kwargs):
        """Get attack GPO script   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attack_settings_gpo_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_attack_settings_gpo_get_with_http_info(x_api_key, **kwargs)
        else:
            (data) = self.api_attack_settings_gpo_get_with_http_info(x_api_key, **kwargs)
            return data

    def api_attack_settings_gpo_get_with_http_info(self, x_api_key, **kwargs):
        """Get attack GPO script   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attack_settings_gpo_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20011
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
                    " to method api_attack_settings_gpo_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_attack_settings_gpo_get`")

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
            'api/attack-settings/gpo', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20011',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_attack_types_get(self, x_api_key, **kwargs):
        """Get attack types   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attack_types_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse2008]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_attack_types_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_attack_types_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_attack_types_get_with_http_info(self, x_api_key, **kwargs):
        """Get attack types   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attack_types_get_with_http_info(x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse2008]
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
                    " to method api_attack_types_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_attack_types_get`")

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
            'api/attack-types', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse2008]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_attacks_get(self, x_api_key, **kwargs):
        """Get all attacks   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse2009]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_attacks_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_attacks_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_attacks_get_with_http_info(self, x_api_key, **kwargs):
        """Get all attacks   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse2009]
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
                    " to method api_attacks_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_attacks_get`")

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
            'api/attacks', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse2009]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_attacks_id_patch(self, body, x_api_key, id, **kwargs):
        """Update attack instance   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_id_patch(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AttacksIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_attacks_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
        else:
            (data) = self.api_attacks_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
            return data

    def api_attacks_id_patch_with_http_info(self, body, x_api_key, id, **kwargs):
        """Update attack instance   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_id_patch_with_http_info(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AttacksIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: Object
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
                    " to method api_attacks_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_attacks_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_attacks_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_attacks_id_patch`")

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
            'api/attacks/{id}', 'PATCH',
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

    def api_attacks_post(self, body, x_api_key, **kwargs):
        """Create attack instance   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_post(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApiAttacksBody body: (required)
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_attacks_post_with_http_info(self,body, x_api_key, **kwargs)
        else:
            (data) = self.api_attacks_post_with_http_info(self,body, x_api_key, **kwargs)
            return data

    def api_attacks_post_with_http_info(self, body, x_api_key, **kwargs):
        """Create attack instance   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_attacks_post_with_http_info(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApiAttacksBody body: (required)
        :param str x_api_key: The user's API key (required)
        :return: InlineResponse20010
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
                    " to method api_attacks_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_attacks_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_attacks_post`")

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
            'api/attacks', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20010',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
