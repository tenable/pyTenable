# coding: utf-8

"""
AboutAPI
========

The following methods allow for interaction into the Tenable.ad
:tenableAD:`about <AboutAPI>` API endpoints.

Methods available on ``tad.about``:

.. rst-class:: hide-signature
.. autoclass:: AboutApi

    .. automethod:: api_about_get

"""

from __future__ import absolute_import
import six
from tenable.ad.api_client import ApiClient as api, ApiClient


class AboutApi(object):
    """
        This is for generating rest calls on the AboutAPI
        Provide general information on Eridanis
    """

    api_client = ApiClient()

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_about_get(self, x_api_key, **kwargs):
        """Get about singleton.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_about_get(self,async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_about_get_with_http_info(self,x_api_key,**kwargs)
        else:
            (data) = self.api_about_get_with_http_info(self,x_api_key,**kwargs)
            return data

    def api_about_get_with_http_info(self, x_api_key, **kwargs):
        """Get about singleton.   

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_about_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_about_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = 'application/json'
        header_params['x-api-key'] = x_api_key
        # Authentication setting
        auth_settings = ['APIKey']

        return self.api_client.call_api(
            'api/about', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse200',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
