# swagger_client.InfrastructureApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_infrastructures_get**](InfrastructureApi.md#api_infrastructures_get) | **GET** /api/infrastructures | Retrieve all infrastructure instances.
[**api_infrastructures_id_delete**](InfrastructureApi.md#api_infrastructures_id_delete) | **DELETE** /api/infrastructures/{id} | Delete infrastructure instance.
[**api_infrastructures_id_get**](InfrastructureApi.md#api_infrastructures_id_get) | **GET** /api/infrastructures/{id} | Get infrastructure instance by id.
[**api_infrastructures_id_patch**](InfrastructureApi.md#api_infrastructures_id_patch) | **PATCH** /api/infrastructures/{id} | Update infrastructure instance.
[**api_infrastructures_post**](InfrastructureApi.md#api_infrastructures_post) | **POST** /api/infrastructures | Create infrastructure instance.

# **api_infrastructures_get**
> list[InlineResponse20026] api_infrastructures_get(x_api_key)

Retrieve all infrastructure instances.

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
api_instance = ad.InfrastructureApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all infrastructure instances.
    api_response = api_instance.api_infrastructures_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InfrastructureApi->api_infrastructures_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20026]**](InlineResponse20026.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_id_delete**
> object api_infrastructures_id_delete(x_api_key, id)

Delete infrastructure instance.

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
api_instance = ad.InfrastructureApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Delete infrastructure instance.
    api_response = api_instance.api_infrastructures_id_delete(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InfrastructureApi->api_infrastructures_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_id_get**
> InlineResponse20026 api_infrastructures_id_get(x_api_key, id)

Get infrastructure instance by id.

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
api_instance = ad.InfrastructureApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get infrastructure instance by id.
    api_response = api_instance.api_infrastructures_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InfrastructureApi->api_infrastructures_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20026**](InlineResponse20026.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_id_patch**
> InlineResponse20027 api_infrastructures_id_patch(body, x_api_key, id)

Update infrastructure instance.

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
api_instance = ad.InfrastructureApi(ad.ApiClient(configuration))
body = ad.InfrastructuresIdBody() # InfrastructuresIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update infrastructure instance.
    api_response = api_instance.api_infrastructures_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InfrastructureApi->api_infrastructures_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**InfrastructuresIdBody**](InfrastructuresIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20027**](InlineResponse20027.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_post**
> list[InlineResponse20026] api_infrastructures_post(body, x_api_key)

Create infrastructure instance.

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
api_instance = ad.InfrastructureApi(ad.ApiClient(configuration))
body = [ad.ApiInfrastructuresBody()] # list[ApiInfrastructuresBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create infrastructure instance.
    api_response = api_instance.api_infrastructures_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InfrastructureApi->api_infrastructures_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApiInfrastructuresBody]**](ApiInfrastructuresBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20026]**](InlineResponse20026.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

