# swagger_client.EventApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_events_event_provider_id_last_events_get**](EventApi.md#api_events_event_provider_id_last_events_get) | **GET** /api/events/{eventProviderId}/last-events | Get the last events for each AD object source and directory
[**api_events_last_get**](EventApi.md#api_events_last_get) | **GET** /api/events/last | Get the last event
[**api_events_search_post**](EventApi.md#api_events_search_post) | **POST** /api/events/search | Search events instances
[**api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get**](EventApi.md#api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/ad-objects/{adObjectId}/events/last | Get the last event related to an AD Object
[**api_infrastructures_infrastructure_id_directories_directory_id_events_id_get**](EventApi.md#api_infrastructures_infrastructure_id_directories_directory_id_events_id_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/events/{id} | Get event instance by id.

# **api_events_event_provider_id_last_events_get**
> list[InlineResponse20025] api_events_event_provider_id_last_events_get(x_api_key, event_provider_id)

Get the last events for each AD object source and directory

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
api_instance = ad.EventApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
event_provider_id = 'event_provider_id_example' # str | 

try:
    # Get the last events for each AD object source and directory
    api_response = api_instance.api_events_event_provider_id_last_events_get(x_api_key, event_provider_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_events_event_provider_id_last_events_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **event_provider_id** | **str**|  | 

### Return type

[**list[InlineResponse20025]**](InlineResponse20025.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_events_last_get**
> InlineResponse20024 api_events_last_get(x_api_key)

Get the last event

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
api_instance = ad.EventApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get the last event
    api_response = api_instance.api_events_last_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_events_last_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20024**](InlineResponse20024.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_events_search_post**
> list[InlineResponse20024] api_events_search_post(body, x_api_key)

Search events instances

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
api_instance = ad.EventApi(ad.ApiClient(configuration))
body = ad.EventsSearchBody() # EventsSearchBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Search events instances
    api_response = api_instance.api_events_search_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_events_search_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventsSearchBody**](EventsSearchBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20024]**](InlineResponse20024.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get**
> InlineResponse20024 api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(x_api_key, infrastructure_id, directory_id, ad_object_id)

Get the last event related to an AD Object

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
api_instance = ad.EventApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
ad_object_id = 'ad_object_id_example' # str | 

try:
    # Get the last event related to an AD Object
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(x_api_key, infrastructure_id, directory_id, ad_object_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **ad_object_id** | **str**|  | 

### Return type

[**InlineResponse20024**](InlineResponse20024.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_events_id_get**
> InlineResponse20024 api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(x_api_key, infrastructure_id, directory_id, id)

Get event instance by id.

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
api_instance = ad.EventApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get event instance by id.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(x_api_key, infrastructure_id, directory_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_infrastructures_infrastructure_id_directories_directory_id_events_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20024**](InlineResponse20024.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

