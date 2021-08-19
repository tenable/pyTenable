"""
DirectoryAPI
========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`directory <DirectoryObject>` API endpoints.

Methods available on ``tad.directory``:

.. rst-class:: hide-signature
.. autoclass:: DirectoryApi

    .. automethod:: api_directories_get
    .. automethod:: api_directories_id_get
    .. automethod:: api_directories_post
    .. automethod:: api_infrastructure_id_directories_get
    .. automethod:: api_infrastructure_id_directories_id_delete
    .. automethod:: api_infrastructure_id_directories_id_get
    .. automethod:: api_infrastructure_id_directories_id_patch

"""
from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class DirectoryApi(object):
    """
        Provide Representation of an Active directory
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_directories_get(self, x_api_key, **kwargs):
        """Retrieve all directory instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20021]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_directories_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_directories_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_directories_get_with_http_info(self, x_api_key, **kwargs):
        """Retrieve all directory instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_get_with_http_info(x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20021]
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
                    " to method api_directories_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_directories_get`")

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
            'api/directories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20021]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_directories_id_get(self, x_api_key, id, **kwargs):
        """Get directory instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_id_get(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20021
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_directories_id_get_with_http_info(self,x_api_key, id, **kwargs)
        else:
            (data) = self.api_directories_id_get_with_http_info(self,x_api_key, id, **kwargs)
            return data

    def api_directories_id_get_with_http_info(self, x_api_key, id, **kwargs):
        """Get directory instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_id_get_with_http_info(self,x_api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :return: InlineResponse20021
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
                    " to method api_directories_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_directories_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `api_directories_id_get`")

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
            'api/directories/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20021',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_directories_post(self, body, x_api_key, **kwargs):
        """Create directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_post(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApiDirectoriesBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20021]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_directories_post_with_http_info(self,body, x_api_key, **kwargs)
        else:
            (data) = self.api_directories_post_with_http_info(self,body, x_api_key, **kwargs)
            return data

    def api_directories_post_with_http_info(self, body, x_api_key, **kwargs):
        """Create directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_directories_post_with_http_info(self,body, x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[ApiDirectoriesBody] body: (required)
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20021]
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
                    " to method api_directories_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `api_directories_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_directories_post`")

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
            'api/directories', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20021]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directories_get(self, x_api_key, infrastructure_id, **kwargs):
        """Get all directories for a given infrastructure   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_get(self,x_api_key, infrastructure_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :return: list[InlineResponse20021]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directories_get_with_http_info(self,x_api_key,
                                                                                             infrastructure_id,
                                                                                             **kwargs)
        else:
            (data) = self.api_infrastructure_id_directories_get_with_http_info(self,x_api_key,
                                                                                               infrastructure_id,
                                                                                               **kwargs)
            return data

    def api_infrastructure_id_directories_get_with_http_info(self, x_api_key, infrastructure_id,
                                                                             **kwargs):
        """Get all directories for a given infrastructure   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_get_with_http_info(self,x_api_key, infrastructure_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :return: list[InlineResponse20021]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_get`")

        collection_formats = {}

        path_params = {}
        if 'infrastructure_id' in params:
            path_params['infrastructureId'] = params['infrastructure_id']

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
            'api/infrastructures/{infrastructureId}/directories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20021]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directories_id_delete(self, x_api_key, infrastructure_id, id, **kwargs):
        """Delete directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_id_delete(self,x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directories_id_delete_with_http_info(self,x_api_key,
                                                                                                   infrastructure_id,
                                                                                                   id, **kwargs)
        else:
            (data) = self.api_infrastructure_id_directories_id_delete_with_http_info(self,x_api_key,
                                                                                                     infrastructure_id,
                                                                                                     id, **kwargs)
            return data

    def api_infrastructure_id_directories_id_delete_with_http_info(self, x_api_key, infrastructure_id,
                                                                                   id, **kwargs):
        """Delete directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_id_delete_with_http_info(self,x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_id_delete`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_id_delete`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_id_delete`")

        collection_formats = {}

        path_params = {}
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
            'api/infrastructures/{infrastructureId}/directories/{id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directories_id_get(self, x_api_key, infrastructure_id, id, **kwargs):
        """Get directory instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_id_get(self,x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse20021
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directories_id_get_with_http_info(self,x_api_key,
                                                                                                infrastructure_id, id,
                                                                                                **kwargs)
        else:
            (data) = self.api_infrastructure_id_directories_id_get_with_http_info(self,x_api_key,
                                                                                                  infrastructure_id, id,
                                                                                                  **kwargs)
            return data

    def api_infrastructure_id_directories_id_get_with_http_info(self, x_api_key, infrastructure_id, id,
                                                                                **kwargs):
        """Get directory instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructures_infrastructure_id_directories_id_get_with_http_info(self,x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse20021
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'infrastructure_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_id_get`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_id_get`")

        collection_formats = {}

        path_params = {}
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
            'api/infrastructures/{infrastructureId}/directories/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20021',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_infrastructure_id_directories_id_patch(self, body, x_api_key, infrastructure_id, id,
                                                                   **kwargs):
        """Update directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_id_patch(self,body, x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DirectoriesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_infrastructure_id_directories_id_patch_with_http_info(self,body, x_api_key,
                                                                                                  infrastructure_id, id,
                                                                                                  **kwargs)
        else:
            (data) = self.api_infrastructure_id_directories_id_patch_with_http_info(self,body, x_api_key,
                                                                                                    infrastructure_id,
                                                                                                    id, **kwargs)
            return data

    def api_infrastructure_id_directories_id_patch_with_http_info(self, body, x_api_key,
                                                                                  infrastructure_id, id, **kwargs):
        """Update directory instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_infrastructure_id_directories_id_patch_with_http_info(self,body, x_api_key, infrastructure_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DirectoriesIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str infrastructure_id: (required)
        :param str id: (required)
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'infrastructure_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_infrastructures_infrastructure_id_directories_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_infrastructures_infrastructure_id_directories_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_infrastructures_infrastructure_id_directories_id_patch`")
            # verify the required parameter 'infrastructure_id' is set
        if ('infrastructure_id' not in params or
                params['infrastructure_id'] is None):
            raise ValueError(
                "Missing the required parameter `infrastructure_id` when calling `api_infrastructures_infrastructure_id_directories_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_infrastructures_infrastructure_id_directories_id_patch`")

        collection_formats = {}

        path_params = {}
        #if 'infrastructure_id' in params:
        #    path_params['infrastructureId'] = params['infrastructure_id']
        #if 'id' in params:
        #    path_params['id'] = params['id']
        url = 'api/infrastructures/' + str(infrastructure_id) + '/directories/' + str(id)
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
            url, 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20022',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
