# swagger_client.ApplicationSettingApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_application_settings_get**](ApplicationSettingApi.md#api_application_settings_get) | **GET** /api/application-settings | Get the application settings
[**api_application_settings_patch**](ApplicationSettingApi.md#api_application_settings_patch) | **PATCH** /api/application-settings | Update the application settings

# **api_application_settings_get**
> InlineResponse2007 api_application_settings_get(x_api_key)

Get the application settings

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
api_instance = ad.ApplicationSettingApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get the application settings
    api_response = api_instance.api_application_settings_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationSettingApi->api_application_settings_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_application_settings_patch**
> InlineResponse2007 api_application_settings_patch(body, x_api_key)

Update the application settings

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
api_instance = ad.ApplicationSettingApi(ad.ApiClient(configuration))
body = ad.ApiApplicationsettingsBody() # ApiApplicationsettingsBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update the application settings
    api_response = api_instance.api_application_settings_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationSettingApi->api_application_settings_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiApplicationsettingsBody**](ApiApplicationsettingsBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

