# swagger_client.ScoreApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_profiles_profile_id_scores_get**](ScoreApi.md#api_profiles_profile_id_scores_get) | **GET** /api/profiles/{profileId}/scores | Get the directories score by profile

# **api_profiles_profile_id_scores_get**
> list[InlineResponse20038] api_profiles_profile_id_scores_get(x_api_key, profile_id)

Get the directories score by profile

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
api_instance = ad.ScoreApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 

try:
    # Get the directories score by profile
    api_response = api_instance.api_profiles_profile_id_scores_get(x_api_key, profile_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScoreApi->api_profiles_profile_id_scores_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 

### Return type

[**list[InlineResponse20038]**](InlineResponse20038.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

