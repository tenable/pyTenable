# swagger_client.PreferenceApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_preferences_get**](PreferenceApi.md#api_preferences_get) | **GET** /api/preferences | Get a user&#x27;s preferences
[**api_preferences_patch**](PreferenceApi.md#api_preferences_patch) | **PATCH** /api/preferences | Update a user&#x27;s preferences

# **api_preferences_get**
> InlineResponse20030 api_preferences_get(x_api_key)

Get a user's preferences

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
api_instance = ad.PreferenceApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get a user's preferences
    api_response = api_instance.api_preferences_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PreferenceApi->api_preferences_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20030**](InlineResponse20030.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_preferences_patch**
> InlineResponse20030 api_preferences_patch(body, x_api_key)

Update a user's preferences

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
api_instance = ad.PreferenceApi(ad.ApiClient(configuration))
body = ad.ApiPreferencesBody() # ApiPreferencesBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update a user's preferences
    api_response = api_instance.api_preferences_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PreferenceApi->api_preferences_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiPreferencesBody**](ApiPreferencesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20030**](InlineResponse20030.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

