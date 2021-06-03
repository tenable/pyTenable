# swagger_client.ReasonApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_profiles_profile_id_checkers_checker_id_reasons_get**](ReasonApi.md#api_profiles_profile_id_checkers_checker_id_reasons_get) | **GET** /api/profiles/{profileId}/checkers/{checkerId}/reasons | Retrieve all reason instances that have deviances for a specific profile and checker.
[**api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get**](ReasonApi.md#api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get) | **GET** /api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/reasons | Retrieve all reason instances for which we have deviances for a specific profile, directory and event.
[**api_reasons_get**](ReasonApi.md#api_reasons_get) | **GET** /api/reasons | Retrieve all reason instances.
[**api_reasons_id_get**](ReasonApi.md#api_reasons_id_get) | **GET** /api/reasons/{id} | Get reason instance by id.

# **api_profiles_profile_id_checkers_checker_id_reasons_get**
> list[InlineResponse20032] api_profiles_profile_id_checkers_checker_id_reasons_get(x_api_key, profile_id, checker_id)

Retrieve all reason instances that have deviances for a specific profile and checker.

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
api_instance = ad.ReasonApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 

try:
    # Retrieve all reason instances that have deviances for a specific profile and checker.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_reasons_get(x_api_key, profile_id, checker_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReasonApi->api_profiles_profile_id_checkers_checker_id_reasons_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 

### Return type

[**list[InlineResponse20032]**](InlineResponse20032.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get**
> list[InlineResponse20032] api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get(x_api_key, profile_id, infrastructure_id, directory_id, event_id)

Retrieve all reason instances for which we have deviances for a specific profile, directory and event.

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
api_instance = ad.ReasonApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
event_id = 'event_id_example' # str | 

try:
    # Retrieve all reason instances for which we have deviances for a specific profile, directory and event.
    api_response = api_instance.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get(x_api_key, profile_id, infrastructure_id, directory_id, event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReasonApi->api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_reasons_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **event_id** | **str**|  | 

### Return type

[**list[InlineResponse20032]**](InlineResponse20032.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_reasons_get**
> list[InlineResponse20032] api_reasons_get(x_api_key)

Retrieve all reason instances.

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
api_instance = ad.ReasonApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all reason instances.
    api_response = api_instance.api_reasons_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReasonApi->api_reasons_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20032]**](InlineResponse20032.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_reasons_id_get**
> InlineResponse20032 api_reasons_id_get(x_api_key, id)

Get reason instance by id.

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
api_instance = ad.ReasonApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get reason instance by id.
    api_response = api_instance.api_reasons_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReasonApi->api_reasons_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20032**](InlineResponse20032.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

