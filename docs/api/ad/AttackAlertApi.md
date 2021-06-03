# swagger_client.AttackAlertApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_alerts_ioa_count_get**](AttackAlertApi.md#api_alerts_ioa_count_get) | **GET** /api/alerts-ioa/count | Get all ioa alerts
[**api_alerts_ioa_get**](AttackAlertApi.md#api_alerts_ioa_get) | **GET** /api/alerts-ioa | Get all ioa alerts
[**api_alerts_ioa_id_patch**](AttackAlertApi.md#api_alerts_ioa_id_patch) | **PATCH** /api/alerts-ioa/{id} | Update an ioa alert instance by ID.
[**api_alerts_ioa_patch**](AttackAlertApi.md#api_alerts_ioa_patch) | **PATCH** /api/alerts-ioa | Update all ioa alerts

# **api_alerts_ioa_count_get**
> InlineResponse20013 api_alerts_ioa_count_get(x_api_key)

Get all ioa alerts

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
api_instance = ad.AttackAlertApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get all ioa alerts
    api_response = api_instance.api_alerts_ioa_count_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAlertApi->api_alerts_ioa_count_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20013**](InlineResponse20013.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_alerts_ioa_get**
> list[InlineResponse20012] api_alerts_ioa_get(x_api_key)

Get all ioa alerts

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
api_instance = ad.AttackAlertApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get all ioa alerts
    api_response = api_instance.api_alerts_ioa_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAlertApi->api_alerts_ioa_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20012]**](InlineResponse20012.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_alerts_ioa_id_patch**
> Object api_alerts_ioa_id_patch(body, x_api_key, id)

Update an ioa alert instance by ID.

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
api_instance = ad.AttackAlertApi(ad.ApiClient(configuration))
body = ad.AlertsioaIdBody() # AlertsioaIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update an ioa alert instance by ID.
    api_response = api_instance.api_alerts_ioa_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAlertApi->api_alerts_ioa_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AlertsioaIdBody**](AlertsioaIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_alerts_ioa_patch**
> Object api_alerts_ioa_patch(body, x_api_key)

Update all ioa alerts

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
api_instance = ad.AttackAlertApi(ad.ApiClient(configuration))
body = ad.ApiAlertsioaBody() # ApiAlertsioaBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update all ioa alerts
    api_response = api_instance.api_alerts_ioa_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAlertApi->api_alerts_ioa_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiAlertsioaBody**](ApiAlertsioaBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

