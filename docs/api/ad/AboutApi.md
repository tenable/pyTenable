# swagger_client.AboutApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_about_get**](AboutApi.md#api_about_get) | **GET** /api/about | Get about singleton.

# **api_about_get**
> InlineResponse200 api_about_get()

Get about singleton.

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ad.AboutApi()

try:
    # Get about singleton.
    api_response = api_instance.api_about_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AboutApi->api_about_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

