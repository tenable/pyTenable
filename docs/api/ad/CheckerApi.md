# swagger_client.CheckerApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_checkers_get**](CheckerApi.md#api_checkers_get) | **GET** /api/checkers | Retrieve all checker instances.
[**api_checkers_id_get**](CheckerApi.md#api_checkers_id_get) | **GET** /api/checkers/{id} | Get checker instance by id.

# **api_checkers_get**
> list[InlineResponse20015] api_checkers_get(x_api_key)

Retrieve all checker instances.

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = ad.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = ad.CheckerApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all checker instances.
    api_response = api_instance.api_checkers_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CheckerApi->api_checkers_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20015]**](InlineResponse20015.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_checkers_id_get**
> InlineResponse20016 api_checkers_id_get(x_api_key, id)

Get checker instance by id.

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = ad.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = ad.CheckerApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get checker instance by id.
    api_response = api_instance.api_checkers_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CheckerApi->api_checkers_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20016**](InlineResponse20016.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

