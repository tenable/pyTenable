# swagger_client.WidgetApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_dashboards_dashboard_id_widgets_get**](WidgetApi.md#api_dashboards_dashboard_id_widgets_get) | **GET** /api/dashboards/{dashboardId}/widgets | Get all widgets by dashboard id
[**api_dashboards_dashboard_id_widgets_id_delete**](WidgetApi.md#api_dashboards_dashboard_id_widgets_id_delete) | **DELETE** /api/dashboards/{dashboardId}/widgets/{id} | Delete widget instance.
[**api_dashboards_dashboard_id_widgets_id_get**](WidgetApi.md#api_dashboards_dashboard_id_widgets_id_get) | **GET** /api/dashboards/{dashboardId}/widgets/{id} | Get widget instance by id.
[**api_dashboards_dashboard_id_widgets_id_options_get**](WidgetApi.md#api_dashboards_dashboard_id_widgets_id_options_get) | **GET** /api/dashboards/{dashboardId}/widgets/{id}/options | Get a widget&#x27;s options by id
[**api_dashboards_dashboard_id_widgets_id_options_put**](WidgetApi.md#api_dashboards_dashboard_id_widgets_id_options_put) | **PUT** /api/dashboards/{dashboardId}/widgets/{id}/options | Define widget&#x27;s options by id
[**api_dashboards_dashboard_id_widgets_id_patch**](WidgetApi.md#api_dashboards_dashboard_id_widgets_id_patch) | **PATCH** /api/dashboards/{dashboardId}/widgets/{id} | Update widget instance.
[**api_dashboards_dashboard_id_widgets_post**](WidgetApi.md#api_dashboards_dashboard_id_widgets_post) | **POST** /api/dashboards/{dashboardId}/widgets | Create a new widget in dashboard by dashboard id
[**api_widgets_get**](WidgetApi.md#api_widgets_get) | **GET** /api/widgets | Retrieve all widget instances.

# **api_dashboards_dashboard_id_widgets_get**
> list[InlineResponse20046] api_dashboards_dashboard_id_widgets_get(x_api_key, dashboard_id)

Get all widgets by dashboard id

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 

try:
    # Get all widgets by dashboard id
    api_response = api_instance.api_dashboards_dashboard_id_widgets_get(x_api_key, dashboard_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 

### Return type

[**list[InlineResponse20046]**](InlineResponse20046.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_id_delete**
> object api_dashboards_dashboard_id_widgets_id_delete(x_api_key, id, dashboard_id)

Delete widget instance.

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 
dashboard_id = 'dashboard_id_example' # str | 

try:
    # Delete widget instance.
    api_response = api_instance.api_dashboards_dashboard_id_widgets_id_delete(x_api_key, id, dashboard_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 
 **dashboard_id** | **str**|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_id_get**
> InlineResponse20046 api_dashboards_dashboard_id_widgets_id_get(x_api_key, dashboard_id, id)

Get widget instance by id.

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get widget instance by id.
    api_response = api_instance.api_dashboards_dashboard_id_widgets_id_get(x_api_key, dashboard_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20046**](InlineResponse20046.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_id_options_get**
> InlineResponse20047 api_dashboards_dashboard_id_widgets_id_options_get(x_api_key, dashboard_id, id)

Get a widget's options by id

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get a widget's options by id
    api_response = api_instance.api_dashboards_dashboard_id_widgets_id_options_get(x_api_key, dashboard_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_id_options_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20047**](InlineResponse20047.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_id_options_put**
> object api_dashboards_dashboard_id_widgets_id_options_put(body, x_api_key, dashboard_id, id)

Define widget's options by id

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
body = ad.IdOptionsBody() # IdOptionsBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 
id = 'id_example' # str | 

try:
    # Define widget's options by id
    api_response = api_instance.api_dashboards_dashboard_id_widgets_id_options_put(body, x_api_key, dashboard_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_id_options_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**IdOptionsBody**](IdOptionsBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_id_patch**
> InlineResponse20046 api_dashboards_dashboard_id_widgets_id_patch(body, x_api_key, dashboard_id, id)

Update widget instance.

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
body = ad.WidgetsIdBody() # WidgetsIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 
id = 'id_example' # str | 

try:
    # Update widget instance.
    api_response = api_instance.api_dashboards_dashboard_id_widgets_id_patch(body, x_api_key, dashboard_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WidgetsIdBody**](WidgetsIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20046**](InlineResponse20046.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_dashboards_dashboard_id_widgets_post**
> InlineResponse20046 api_dashboards_dashboard_id_widgets_post(body, x_api_key, dashboard_id)

Create a new widget in dashboard by dashboard id

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
body = ad.DashboardIdWidgetsBody() # DashboardIdWidgetsBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
dashboard_id = 'dashboard_id_example' # str | 

try:
    # Create a new widget in dashboard by dashboard id
    api_response = api_instance.api_dashboards_dashboard_id_widgets_post(body, x_api_key, dashboard_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_dashboards_dashboard_id_widgets_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DashboardIdWidgetsBody**](DashboardIdWidgetsBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **dashboard_id** | **str**|  | 

### Return type

[**InlineResponse20046**](InlineResponse20046.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_widgets_get**
> list[InlineResponse20046] api_widgets_get(x_api_key)

Retrieve all widget instances.

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
api_instance = ad.WidgetApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all widget instances.
    api_response = api_instance.api_widgets_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WidgetApi->api_widgets_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20046]**](InlineResponse20046.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

