# swagger_client.ADObjectApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get**](ADObjectApi.md#api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/ad-objects/{id} | Get ad-object instance by id.
[**api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get**](ADObjectApi.md#api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/ad-objects/{id}/changes | Get one ad-object changes between a given event and the event which precedes it
[**api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get**](ADObjectApi.md#api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/ad-objects/{id} | Get ad-object instance by id.
[**api_profiles_profile_id_checkers_checker_id_ad_objects_id_get**](ADObjectApi.md#api_profiles_profile_id_checkers_checker_id_ad_objects_id_get) | **GET** /api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{id} | Retrieve an AD object by id that have deviances for a specific profile and checker
[**api_profiles_profile_id_checkers_checker_id_ad_objects_search_post**](ADObjectApi.md#api_profiles_profile_id_checkers_checker_id_ad_objects_search_post) | **POST** /api/profiles/{profileId}/checkers/{checkerId}/ad-objects/search | Search all AD objects having deviances by profile by checker

# **api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get**
> InlineResponse2001 api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get(x_api_key, directory_id, infrastructure_id, id)

Get ad-object instance by id.

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
api_instance = ad.ADObjectApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
directory_id = 'directory_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get ad-object instance by id.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get(x_api_key, directory_id, infrastructure_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ADObjectApi->api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **directory_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get**
> list[InlineResponse2003] api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get(x_api_key, infrastructure_id, directory_id, event_id, id, wanted_values=wanted_values, event_provider_id=event_provider_id)

Get one ad-object changes between a given event and the event which precedes it

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
api_instance = ad.ADObjectApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
event_id = 'event_id_example' # str | 
id = 'id_example' # str | 
wanted_values = ['wanted_values_example'] # list[str] |  (optional)
event_provider_id = 'event_provider_id_example' # str |  (optional)

try:
    # Get one ad-object changes between a given event and the event which precedes it
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get(x_api_key, infrastructure_id, directory_id, event_id, id, wanted_values=wanted_values, event_provider_id=event_provider_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ADObjectApi->api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_changes_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **event_id** | **str**|  | 
 **id** | **str**|  | 
 **wanted_values** | [**list[str]**](str.md)|  | [optional] 
 **event_provider_id** | **str**|  | [optional] 

### Return type

[**list[InlineResponse2003]**](InlineResponse2003.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get**
> InlineResponse2001 api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get(x_api_key, directory_id, infrastructure_id, id, event_id)

Get ad-object instance by id.

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
api_instance = ad.ADObjectApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
directory_id = 'directory_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
id = 'id_example' # str | 
event_id = 'event_id_example' # str | 

try:
    # Get ad-object instance by id.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get(x_api_key, directory_id, infrastructure_id, id, event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ADObjectApi->api_infrastructures_infrastructure_id_directories_directory_id_events_event_id_ad_objects_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **directory_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **id** | **str**|  | 
 **event_id** | **str**|  | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_ad_objects_id_get**
> InlineResponse2002 api_profiles_profile_id_checkers_checker_id_ad_objects_id_get(x_api_key, profile_id, checker_id, id, show_ignored=show_ignored)

Retrieve an AD object by id that have deviances for a specific profile and checker

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
api_instance = ad.ADObjectApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
id = 'id_example' # str | 
show_ignored = 'show_ignored_example' # str |  (optional)

try:
    # Retrieve an AD object by id that have deviances for a specific profile and checker
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_ad_objects_id_get(x_api_key, profile_id, checker_id, id, show_ignored=show_ignored)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ADObjectApi->api_profiles_profile_id_checkers_checker_id_ad_objects_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **id** | **str**|  | 
 **show_ignored** | **str**|  | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_ad_objects_search_post**
> list[InlineResponse2004] api_profiles_profile_id_checkers_checker_id_ad_objects_search_post(body, x_api_key, profile_id, checker_id, per_page=per_page, page=page)

Search all AD objects having deviances by profile by checker

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
api_instance = ad.ADObjectApi(ad.ApiClient(configuration))
body = ad.AdobjectsSearchBody() # AdobjectsSearchBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Search all AD objects having deviances by profile by checker
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_ad_objects_search_post(body, x_api_key, profile_id, checker_id, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ADObjectApi->api_profiles_profile_id_checkers_checker_id_ad_objects_search_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AdobjectsSearchBody**](AdobjectsSearchBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse2004]**](InlineResponse2004.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

