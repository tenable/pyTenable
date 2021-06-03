# swagger_client.CheckerOptionApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_profiles_profile_id_checkers_checker_id_checker_options_get**](CheckerOptionApi.md#api_profiles_profile_id_checkers_checker_id_checker_options_get) | **GET** /api/profiles/{profileId}/checkers/{checkerId}/checker-options | Get all checker options related to a checker.
[**api_profiles_profile_id_checkers_checker_id_checker_options_post**](CheckerOptionApi.md#api_profiles_profile_id_checkers_checker_id_checker_options_post) | **POST** /api/profiles/{profileId}/checkers/{checkerId}/checker-options | Create checker options related to a checker.

# **api_profiles_profile_id_checkers_checker_id_checker_options_get**
> list[InlineResponse20017] api_profiles_profile_id_checkers_checker_id_checker_options_get(x_api_key, profile_id, checker_id, staged=staged, per_page=per_page, page=page)

Get all checker options related to a checker.

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
api_instance = ad.CheckerOptionApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
staged = 'staged_example' # str |  (optional)
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Get all checker options related to a checker.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_checker_options_get(x_api_key, profile_id, checker_id, staged=staged, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CheckerOptionApi->api_profiles_profile_id_checkers_checker_id_checker_options_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **staged** | **str**|  | [optional] 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20017]**](InlineResponse20017.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_checker_options_post**
> list[InlineResponse20017] api_profiles_profile_id_checkers_checker_id_checker_options_post(body, x_api_key, profile_id, checker_id)

Create checker options related to a checker.

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
api_instance = ad.CheckerOptionApi(ad.ApiClient(configuration))
body = [ad.CheckerIdCheckeroptionsBody()] # list[CheckerIdCheckeroptionsBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 

try:
    # Create checker options related to a checker.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_checker_options_post(body, x_api_key, profile_id, checker_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CheckerOptionApi->api_profiles_profile_id_checkers_checker_id_checker_options_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[CheckerIdCheckeroptionsBody]**](CheckerIdCheckeroptionsBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 

### Return type

[**list[InlineResponse20017]**](InlineResponse20017.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

