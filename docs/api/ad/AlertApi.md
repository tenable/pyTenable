# swagger_client.AlertApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_alerts_id_get**](AlertApi.md#api_alerts_id_get) | **GET** /api/alerts/{id} | Get alert instance by id.
[**api_alerts_id_patch**](AlertApi.md#api_alerts_id_patch) | **PATCH** /api/alerts/{id} | Update alert instance.
[**api_profiles_profile_id_alerts_get**](AlertApi.md#api_profiles_profile_id_alerts_get) | **GET** /api/profiles/{profileId}/alerts | Retrieve all alert instances.
[**api_profiles_profile_id_alerts_patch**](AlertApi.md#api_profiles_profile_id_alerts_patch) | **PATCH** /api/profiles/{profileId}/alerts | Update alerts for one profile

# **api_alerts_id_get**
> InlineResponse2005 api_alerts_id_get(x_api_key, id)

Get alert instance by id.

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
api_instance = ad.AlertApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get alert instance by id.
    api_response = api_instance.api_alerts_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertApi->api_alerts_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_alerts_id_patch**
> InlineResponse2005 api_alerts_id_patch(body, x_api_key, id)

Update alert instance.

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
api_instance = ad.AlertApi(ad.ApiClient(configuration))
body = ad.AlertsIdBody() # AlertsIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update alert instance.
    api_response = api_instance.api_alerts_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertApi->api_alerts_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AlertsIdBody**](AlertsIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_alerts_get**
> list[InlineResponse2005] api_profiles_profile_id_alerts_get(x_api_key, profile_id, archived=archived, read=read, per_page=per_page, page=page)

Retrieve all alert instances.

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
api_instance = ad.AlertApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 
archived = 'archived_example' # str |  (optional)
read = 'read_example' # str |  (optional)
per_page = 'per_page_example' # str |  (optional)
page = 'page_example' # str |  (optional)

try:
    # Retrieve all alert instances.
    api_response = api_instance.api_profiles_profile_id_alerts_get(x_api_key, profile_id, archived=archived, read=read, per_page=per_page, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertApi->api_profiles_profile_id_alerts_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 
 **archived** | **str**|  | [optional] 
 **read** | **str**|  | [optional] 
 **per_page** | **str**|  | [optional] 
 **page** | **str**|  | [optional] 

### Return type

[**list[InlineResponse2005]**](InlineResponse2005.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_profile_id_alerts_patch**
> Object api_profiles_profile_id_alerts_patch(body, x_api_key, profile_id)

Update alerts for one profile

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
api_instance = ad.AlertApi(ad.ApiClient(configuration))
body = ad.ProfileIdAlertsBody() # ProfileIdAlertsBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
profile_id = 'profile_id_example' # str | 

try:
    # Update alerts for one profile
    api_response = api_instance.api_profiles_profile_id_alerts_patch(body, x_api_key, profile_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertApi->api_profiles_profile_id_alerts_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProfileIdAlertsBody**](ProfileIdAlertsBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **profile_id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

