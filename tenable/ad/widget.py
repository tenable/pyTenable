"""
WidgetApi
=============

The following methods allow for interaction into the Tenable.ad
:tenableAD:`widget <WidgetObject>` API endpoints.

Methods available on ``tad.widget``:

.. rst-class:: hide-signature
.. autoclass:: WidgetApi

    .. automethod:: api_dashboards_dashboard_id_widgets_get
    .. automethod:: api_dashboards_dashboard_id_widgets_id_delete
    .. automethod:: api_dashboards_dashboard_id_widgets_id_get
    .. automethod:: aapi_dashboards_dashboard_id_widgets_id_options_get
    .. automethod:: api_dashboards_dashboard_id_widgets_id_options_put
    .. automethod:: api_dashboards_dashboard_id_widgets_id_patch
    .. automethod:: api_dashboards_dashboard_id_widgets_post
    .. automethod:: api_widgets_get

"""

from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tenable.ad.api_client import ApiClient


class WidgetApi(object):
    """
        Provide api for dashboard and widget of series of data
    """
    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_dashboards_dashboard_id_widgets_get(self, x_api_key, dashboard_id, **kwargs):
        """Get all widgets by dashboard id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_get(self,x_api_key, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :return: list[InlineResponse20046]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_get_with_http_info(self,x_api_key, dashboard_id, **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_get_with_http_info(self,x_api_key, dashboard_id, **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_get_with_http_info(self, x_api_key, dashboard_id, **kwargs):
        """Get all widgets by dashboard id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_get_with_http_info(self,x_api_key, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :return: list[InlineResponse20046]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'dashboard_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_get`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_get`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']

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
            'api/dashboards/{dashboardId}/widgets', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20046]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_dashboards_dashboard_id_widgets_id_delete(self, x_api_key, id, dashboard_id, **kwargs):
        """Delete widget instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_delete(self,x_api_key, id, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :param str dashboard_id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_id_delete_with_http_info(self,x_api_key, id, dashboard_id,
                                                                                     **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_id_delete_with_http_info(self,x_api_key, id, dashboard_id,
                                                                                       **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_id_delete_with_http_info(self, x_api_key, id, dashboard_id, **kwargs):
        """Delete widget instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_delete_with_http_info(self,x_api_key, id, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str id: (required)
        :param str dashboard_id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'id', 'dashboard_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_id_delete`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_dashboards_dashboard_id_widgets_id_delete`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_id_delete`")

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']

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
            'api/dashboards/{dashboardId}/widgets/{id}', 'DELETE',
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

    def api_dashboards_dashboard_id_widgets_id_get(self, x_api_key, dashboard_id, id, **kwargs):
        """Get widget instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_get(self,x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_id_get_with_http_info(self,x_api_key, dashboard_id, id, **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_id_get_with_http_info(self,x_api_key, dashboard_id, id,
                                                                                    **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_id_get_with_http_info(self, x_api_key, dashboard_id, id, **kwargs):
        """Get widget instance by id.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_get_with_http_info(self,x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'dashboard_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_id_get`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_id_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_dashboards_dashboard_id_widgets_id_get`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']
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
            'api/dashboards/{dashboardId}/widgets/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20046',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_dashboards_dashboard_id_widgets_id_options_get(self, x_api_key, dashboard_id, id, **kwargs):
        """Get a widget's options by id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_options_get(self,x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20047
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_id_options_get_with_http_info(self,x_api_key, dashboard_id, id,
                                                                                          **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_id_options_get_with_http_info(self,x_api_key, dashboard_id, id,
                                                                                            **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_id_options_get_with_http_info(self, x_api_key, dashboard_id, id, **kwargs):
        """Get a widget's options by id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_options_get_with_http_info(self,x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20047
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_api_key', 'dashboard_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_id_options_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_id_options_get`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_id_options_get`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_dashboards_dashboard_id_widgets_id_options_get`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']
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
            'api/dashboards/{dashboardId}/widgets/{id}/options', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20047',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_dashboards_dashboard_id_widgets_id_options_put(self, body, x_api_key, dashboard_id, id, **kwargs):
        """Define widget's options by id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_options_put(self,body, x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param IdOptionsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_id_options_put_with_http_info(self,body, x_api_key, dashboard_id,
                                                                                          id, **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_id_options_put_with_http_info(self,body, x_api_key,
                                                                                            dashboard_id, id, **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_id_options_put_with_http_info(self, body, x_api_key, dashboard_id, id,
                                                                          **kwargs):
        """Define widget's options by id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_options_put_with_http_info(self,body, x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param IdOptionsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'dashboard_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_id_options_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_dashboards_dashboard_id_widgets_id_options_put`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_id_options_put`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_id_options_put`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_dashboards_dashboard_id_widgets_id_options_put`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']
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
            'api/dashboards/{dashboardId}/widgets/{id}/options', 'PUT',
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

    def api_dashboards_dashboard_id_widgets_id_patch(self, body, x_api_key, dashboard_id, id, **kwargs):
        """Update widget instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_patch(self,body, x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param WidgetsIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_id_patch_with_http_info(self,body, x_api_key, dashboard_id, id,
                                                                                    **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_id_patch_with_http_info(self,body, x_api_key, dashboard_id, id,
                                                                                      **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_id_patch_with_http_info(self, body, x_api_key, dashboard_id, id, **kwargs):
        """Update widget instance.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_id_patch_with_http_info(self,body, x_api_key, dashboard_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param WidgetsIdBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :param str id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'dashboard_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_id_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_dashboards_dashboard_id_widgets_id_patch`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_id_patch`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_id_patch`")
            # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError(
                "Missing the required parameter `id` when calling `api_dashboards_dashboard_id_widgets_id_patch`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']
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
            'api/dashboards/{dashboardId}/widgets/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20046',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_dashboards_dashboard_id_widgets_post(self, body, x_api_key, dashboard_id, **kwargs):
        """Create a new widget in dashboard by dashboard id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_post(self,body, x_api_key, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DashboardIdWidgetsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_dashboards_dashboard_id_widgets_post_with_http_info(self,body, x_api_key, dashboard_id, **kwargs)
        else:
            (data) = self.api_dashboards_dashboard_id_widgets_post_with_http_info(self,body, x_api_key, dashboard_id,
                                                                                  **kwargs)
            return data

    def api_dashboards_dashboard_id_widgets_post_with_http_info(self, body, x_api_key, dashboard_id, **kwargs):
        """Create a new widget in dashboard by dashboard id   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_dashboards_dashboard_id_widgets_post_with_http_info(self,body, x_api_key, dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DashboardIdWidgetsBody body: (required)
        :param str x_api_key: The user's API key (required)
        :param str dashboard_id: (required)
        :return: InlineResponse20046
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_api_key', 'dashboard_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_dashboards_dashboard_id_widgets_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError(
                "Missing the required parameter `body` when calling `api_dashboards_dashboard_id_widgets_post`")
            # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError(
                "Missing the required parameter `x_api_key` when calling `api_dashboards_dashboard_id_widgets_post`")
            # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError(
                "Missing the required parameter `dashboard_id` when calling `api_dashboards_dashboard_id_widgets_post`")

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboardId'] = params['dashboard_id']

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
            'api/dashboards/{dashboardId}/widgets', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20046',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_widgets_get(self, x_api_key, **kwargs):
        """Retrieve all widget instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_widgets_get(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20046]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_widgets_get_with_http_info(self,x_api_key, **kwargs)
        else:
            (data) = self.api_widgets_get_with_http_info(self,x_api_key, **kwargs)
            return data

    def api_widgets_get_with_http_info(self, x_api_key, **kwargs):
        """Retrieve all widget instances.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_widgets_get_with_http_info(self,x_api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_api_key: The user's API key (required)
        :return: list[InlineResponse20046]
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
                    " to method api_widgets_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_api_key' is set
        if ('x_api_key' not in params or
                params['x_api_key'] is None):
            raise ValueError("Missing the required parameter `x_api_key` when calling `api_widgets_get`")

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
            'api/widgets', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InlineResponse20046]',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
