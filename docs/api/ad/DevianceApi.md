# swagger_client.DevianceApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_infrastructures_infrastructure_id_directories_directory_id_deviances_get**](DevianceApi.md#api_infrastructures_infrastructure_id_directories_directory_id_deviances_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances | Get all deviances for a directory.
[**api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get**](DevianceApi.md#api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances/{id} | Get ad-object-deviance-history instance by id.
[**api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch**](DevianceApi.md#api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch) | **PATCH** /api/infrastructures/{infrastructureId}/directories/{directoryId}/deviances/{id} | Update ad-object-deviance-history instance.
[**api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch**](DevianceApi.md#api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch) | **PATCH** /api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{adObjectId}/deviances | Update instances matching a checkerId and an AD object ID.
[**api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post**](DevianceApi.md#api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post) | **POST** /api/profiles/{profileId}/checkers/{checkerId}/ad-objects/{adObjectId}/deviances | Search all deviances by profile by checker by AD object
[**api_profiles_profile_id_checkers_checker_id_deviances_patch**](DevianceApi.md#api_profiles_profile_id_checkers_checker_id_deviances_patch) | **PATCH** /api/profiles/{profileId}/checkers/{checkerId}/deviances | Update instances matching a checkerId.
[**api_profiles_profile_id_checkers_checker_id_deviances_post**](DevianceApi.md#api_profiles_profile_id_checkers_checker_id_deviances_post) | **POST** /api/profiles/{profileId}/checkers/{checkerId}/deviances | Get all deviances by checker.
[**api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get**](DevianceApi.md#api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get) | **GET** /api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/checkers/{checkerId}/deviances | Get all deviances related to a single directory and checker.
[**api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post**](DevianceApi.md#api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post) | **POST** /api/profiles/{profileId}/infrastructures/{infrastructureId}/directories/{directoryId}/events/{eventId}/deviances | Get all deviances by eventId.

# **api_infrastructures_infrastructure_id_directories_directory_id_deviances_get**
> list[InlineResponse20019] api_infrastructures_infrastructure_id_directories_directory_id_deviances_get(x_api_key, directory_id, infrastructure_id, page=page, per_page=per_page, batch_size=batch_size, last_identifier_seen=last_identifier_seen, resolved=resolved)

Get all deviances for a directory.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
directory_id = 'directory_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
page = 'page_example' # str |  (optional)
per_page = 'per_page_example' # str |  (optional)
batch_size = 'batch_size_example' # str |  (optional)
last_identifier_seen = 'last_identifier_seen_example' # str |  (optional)
resolved = 'resolved_example' # str |  (optional)

try:
    # Get all deviances for a directory.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_deviances_get(x_api_key, directory_id, infrastructure_id, page=page, per_page=per_page, batch_size=batch_size, last_identifier_seen=last_identifier_seen, resolved=resolved)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_infrastructures_infrastructure_id_directories_directory_id_deviances_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **directory_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **page** | **str**|  | [optional] 
 **per_page** | **str**|  | [optional] 
 **batch_size** | **str**|  | [optional] 
 **last_identifier_seen** | **str**|  | [optional] 
 **resolved** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20019]**](InlineResponse20019.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get**
> InlineResponse20020 api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get(x_api_key, infrastructure_id, directory_id, id)

Get ad-object-deviance-history instance by id.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get ad-object-deviance-history instance by id.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get(x_api_key, infrastructure_id, directory_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20020**](InlineResponse20020.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch**
> InlineResponse20020 api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch(body, x_api_key, infrastructure_id, directory_id, id)

Update ad-object-deviance-history instance.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.DeviancesIdBody() # DeviancesIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
id = 'id_example' # str | 

try:
    # Update ad-object-deviance-history instance.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch(body, x_api_key, infrastructure_id, directory_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_infrastructures_infrastructure_id_directories_directory_id_deviances_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeviancesIdBody**](DeviancesIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20020**](InlineResponse20020.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch**
> Object api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch(body, x_api_key, profile_id, checker_id, ad_object_id)

Update instances matching a checkerId and an AD object ID.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.AdObjectIdDeviancesBody1() # AdObjectIdDeviancesBody1 | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
ad_object_id = 'ad_object_id_example' # str | 

try:
    # Update instances matching a checkerId and an AD object ID.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch(body, x_api_key, profile_id, checker_id, ad_object_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AdObjectIdDeviancesBody1**](AdObjectIdDeviancesBody1.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **ad_object_id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post**
> list[InlineResponse20019] api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post(body, x_api_key, profile_id, checker_id, ad_object_id, per_page=per_page, page=page)

Search all deviances by profile by checker by AD object

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.AdObjectIdDeviancesBody() # AdObjectIdDeviancesBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
ad_object_id = 'ad_object_id_example' # str | 
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Search all deviances by profile by checker by AD object
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post(body, x_api_key, profile_id, checker_id, ad_object_id, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_checkers_checker_id_ad_objects_ad_object_id_deviances_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AdObjectIdDeviancesBody**](AdObjectIdDeviancesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **ad_object_id** | **str**|  | 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20019]**](InlineResponse20019.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_deviances_patch**
> Object api_profiles_profile_id_checkers_checker_id_deviances_patch(body, x_api_key, profile_id, checker_id)

Update instances matching a checkerId.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.CheckerIdDeviancesBody1() # CheckerIdDeviancesBody1 | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 

try:
    # Update instances matching a checkerId.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_deviances_patch(body, x_api_key, profile_id, checker_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_checkers_checker_id_deviances_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CheckerIdDeviancesBody1**](CheckerIdDeviancesBody1.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_checkers_checker_id_deviances_post**
> list[InlineResponse20019] api_profiles_profile_id_checkers_checker_id_deviances_post(body, x_api_key, profile_id, checker_id, per_page=per_page, page=page, batch_size=batch_size, last_identifier_seen=last_identifier_seen)

Get all deviances by checker.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.CheckerIdDeviancesBody() # CheckerIdDeviancesBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
checker_id = 'checker_id_example' # str | 
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)
batch_size = 'batch_size_example' # str |  (optional)
last_identifier_seen = 'last_identifier_seen_example' # str |  (optional)

try:
    # Get all deviances by checker.
    api_response = api_instance.api_profiles_profile_id_checkers_checker_id_deviances_post(body, x_api_key, profile_id, checker_id, per_page=per_page, page=page, batch_size=batch_size, last_identifier_seen=last_identifier_seen)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_checkers_checker_id_deviances_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CheckerIdDeviancesBody**](CheckerIdDeviancesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 
 **batch_size** | **str**|  | [optional] 
 **last_identifier_seen** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20019]**](InlineResponse20019.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get**
> list[InlineResponse20019] api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get(x_api_key, profile_id, infrastructure_id, directory_id, checker_id, per_page=per_page, page=page)

Get all deviances related to a single directory and checker.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
checker_id = 'checker_id_example' # str | 
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Get all deviances related to a single directory and checker.
    api_response = api_instance.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get(x_api_key, profile_id, infrastructure_id, directory_id, checker_id, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_checkers_checker_id_deviances_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **checker_id** | **str**|  | 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20019]**](InlineResponse20019.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post**
> list[InlineResponse20019] api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post(body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, per_page=per_page, page=page)

Get all deviances by eventId.

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
api_instance = ad.DevianceApi(ad.ApiClient(configuration))
body = ad.EventIdDeviancesBody() # EventIdDeviancesBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
infrastructure_id = 'infrastructure_id_example' # str | 
directory_id = 'directory_id_example' # str | 
event_id = 'event_id_example' # str | 
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Get all deviances by eventId.
    api_response = api_instance.api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post(body, x_api_key, profile_id, infrastructure_id, directory_id, event_id, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevianceApi->api_profiles_profile_id_infrastructures_infrastructure_id_directories_directory_id_events_event_id_deviances_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventIdDeviancesBody**](EventIdDeviancesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **infrastructure_id** | **str**|  | 
 **directory_id** | **str**|  | 
 **event_id** | **str**|  | 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse20019]**](InlineResponse20019.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

