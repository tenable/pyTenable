"""
RoleApi
=============

The following methods allow for interaction into the Tenable.ad
:tenableAD:`role <RoleObject>` API endpoints.

Methods available on ``tad.role``:

.. rst-class:: hide-signature
.. autoclass:: RoleApi

    .. automethod:: api_roles_from_from_id_post
    .. automethod:: api_roles_get
    .. automethod:: api_roles_id_get
    .. automethod:: api_roles_id_patch
    .. automethod:: api_roles_id_permissions_put
    .. automethod:: api_roles_post
    .. automethod:: api_roles_user_creation_defaults_get

"""
from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class RoleApi(object):
    """
        Provide Groupment of permissions that may be assigned to several users
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_roles_from_from_id_post(self, body, x_api_key, from_id, **kwargs):
        """Creates a new role from another one   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_from_from_id_post(self,body, x_api_key, from_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FromFromIdBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str from_id: (required)
        :return: InlineResponse204
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_from_from_id_post_with_http_info(self,body, x_api_key, from_id, **kwargs)
        else:
            (data) = self.api_roles_from_from_id_post_with_http_info(self,body, x_api_key, from_id, **kwargs)
            return data

    def api_roles_from_from_id_post_with_http_info(self, body, x_api_key, from_id, **kwargs):
        """Creates a new role from another one   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_from_from_id_post_with_http_info(self,body, x_api_key, from_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FromFromIdBody1 body: (required)
        :param str x_api_key: The user's API key (required)
        :param str from_id: (required)
        :return: InlineResponse204
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'from_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_roles_from_from_id_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_roles_from_from_id_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_from_from_id_post`")
            # verify the required parameter 'from_id' is set
        if ('from_id' not in params or
                params['from_id'] is None):
            raise ValueError("Missing the required parameter `from_id` when calling `api_roles_from_from_id_post`")

        collection_formats = {}

        path_params = {}
        if 'from_id' in params:
            path_params['fromId'] = params['from_id']

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
            'api/roles/from/{fromId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse204',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_get(self, x_api_key, **kwargs):
        """Retrieve all role instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_roles_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_roles_get_with_http_info(self, x_api_key, **kwargs):
        """Retrieve all role instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
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
                    " to method api_roles_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_get`")

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
            'api/roles', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20033]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_id_delete(self, x_api_key, id, **kwargs):
        """Delete role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_delete(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: Object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_id_delete_with_http_info(self,x_api_key, id, **kwargs)
        else:
            (data) = self.api_roles_id_delete_with_http_info(self,x_api_key, id, **kwargs)
            return data

    def api_roles_id_delete_with_http_info(self, x_api_key, id, **kwargs):
        """Delete role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_delete_with_http_info(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: Object
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
                    " to method api_roles_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_id_delete`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_roles_id_delete`")

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
            'api/roles/{id}', 'DELETE',
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

    def api_roles_id_get(self, x_api_key, id, **kwargs):
        """Get role instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_get(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20034
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_id_get_with_http_info(self,x_api_key, id, **kwargs)
        else:
            (data) = self.api_roles_id_get_with_http_info(self,x_api_key, id, **kwargs)
            return data

    def api_roles_id_get_with_http_info(self, x_api_key, id, **kwargs):
        """Get role instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_get_with_http_info(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20034
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
                    " to method api_roles_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_roles_id_get`")

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
            'api/roles/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20034',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_id_patch(self, body, x_api_key, id, **kwargs):
        """Update role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_patch(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RolesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20035
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
        else:
            (data) = self.api_roles_id_patch_with_http_info(self,body, x_api_key, id, **kwargs)
            return data

    def api_roles_id_patch_with_http_info(self, body, x_api_key, id, **kwargs):
        """Update role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_patch_with_http_info(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RolesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20035
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
                    " to method api_roles_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_roles_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_roles_id_patch`")

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
            'api/roles/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20035',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_id_permissions_put(self, body, x_api_key, id, **kwargs):
        """Replace permission list for a role   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_permissions_put(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApirolesPermissions] body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse204
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_id_permissions_put_with_http_info(self,body, x_api_key, id, **kwargs)
        else:
            (data) = self.api_roles_id_permissions_put_with_http_info(self,body, x_api_key, id, **kwargs)
            return data

    def api_roles_id_permissions_put_with_http_info(self, body, x_api_key, id, **kwargs):
        """Replace permission list for a role   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_id_permissions_put_with_http_info(self,body, x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApirolesPermissions] body: (required)
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse204
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
                    " to method api_roles_id_permissions_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_roles_id_permissions_put`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_id_permissions_put`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_roles_id_permissions_put`")

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
            'api/roles/{id}/permissions', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse204',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_post(self, body, x_api_key, **kwargs):
        """Create role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_post(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApiRolesBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_post_with_http_info(self,body, x_api_key, **kwargs)
        else:
            (data) = self.api_roles_post_with_http_info(self,body, x_api_key, **kwargs)
            return data

    def api_roles_post_with_http_info(self, body, x_api_key, **kwargs):
        """Create role instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_post_with_http_info(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApiRolesBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
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
                    " to method api_roles_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_roles_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_roles_post`")

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
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['ApiKey']

        return self.api_client.call_api(
            'api/roles', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20033]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_roles_user_creation_defaults_get(self, x_api_key, **kwargs):
        """Return the default roles for user creation   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_user_creation_defaults_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_roles_user_creation_defaults_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_roles_user_creation_defaults_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_roles_user_creation_defaults_get_with_http_info(self, x_api_key, **kwargs):
        """Return the default roles for user creation   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_roles_user_creation_defaults_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20033]
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
                    " to method api_roles_user_creation_defaults_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_roles_user_creation_defaults_get`")

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
            'api/roles/user-creation-defaults', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20033]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
