# swagger_client.DirectoryApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_directories_get**](DirectoryApi.md#api_directories_get) | **GET** /api/directories | Retrieve all directory instances.
[**api_directories_id_get**](DirectoryApi.md#api_directories_id_get) | **GET** /api/directories/{id} | Get directory instance by id.
[**api_directories_post**](DirectoryApi.md#api_directories_post) | **POST** /api/directories | Create directory instance.
[**api_infrastructures_infrastructure_id_directories_get**](DirectoryApi.md#api_infrastructures_infrastructure_id_directories_get) | **GET** /api/infrastructures/{infrastructureId}/directories | Get all directories for a given infrastructure
[**api_infrastructures_infrastructure_id_directories_id_delete**](DirectoryApi.md#api_infrastructures_infrastructure_id_directories_id_delete) | **DELETE** /api/infrastructures/{infrastructureId}/directories/{id} | Delete directory instance.
[**api_infrastructures_infrastructure_id_directories_id_get**](DirectoryApi.md#api_infrastructures_infrastructure_id_directories_id_get) | **GET** /api/infrastructures/{infrastructureId}/directories/{id} | Get directory instance by id.
[**api_infrastructures_infrastructure_id_directories_id_patch**](DirectoryApi.md#api_infrastructures_infrastructure_id_directories_id_patch) | **PATCH** /api/infrastructures/{infrastructureId}/directories/{id} | Update directory instance.

# **api_directories_get**
> list[InlineResponse20021] api_directories_get(x_api_key)

Retrieve all directory instances.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all directory instances.
    api_response = api_instance.api_directories_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_directories_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20021]**](InlineResponse20021.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_directories_id_get**
> InlineResponse20021 api_directories_id_get(x_api_key, id)

Get directory instance by id.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get directory instance by id.
    api_response = api_instance.api_directories_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_directories_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20021**](InlineResponse20021.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_directories_post**
> list[InlineResponse20021] api_directories_post(body, x_api_key)

Create directory instance.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
body = [ad.ApiDirectoriesBody()] # list[ApiDirectoriesBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create directory instance.
    api_response = api_instance.api_directories_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_directories_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApiDirectoriesBody]**](ApiDirectoriesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20021]**](InlineResponse20021.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_get**
> list[InlineResponse20021] api_infrastructures_infrastructure_id_directories_get(x_api_key, infrastructure_id)

Get all directories for a given infrastructure

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 

try:
    # Get all directories for a given infrastructure
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_get(x_api_key, infrastructure_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_infrastructures_infrastructure_id_directories_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 

### Return type

[**list[InlineResponse20021]**](InlineResponse20021.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_id_delete**
> object api_infrastructures_infrastructure_id_directories_id_delete(x_api_key, infrastructure_id, id)

Delete directory instance.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
id = 'id_example' # str | 

try:
    # Delete directory instance.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_id_delete(x_api_key, infrastructure_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_infrastructures_infrastructure_id_directories_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_id_get**
> InlineResponse20021 api_infrastructures_infrastructure_id_directories_id_get(x_api_key, infrastructure_id, id)

Get directory instance by id.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get directory instance by id.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_id_get(x_api_key, infrastructure_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_infrastructures_infrastructure_id_directories_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20021**](InlineResponse20021.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_infrastructures_infrastructure_id_directories_id_patch**
> InlineResponse20022 api_infrastructures_infrastructure_id_directories_id_patch(body, x_api_key, infrastructure_id, id)

Update directory instance.

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
api_instance = ad.DirectoryApi(ad.ApiClient(configuration))
body = ad.DirectoriesIdBody() # DirectoriesIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
infrastructure_id = 'infrastructure_id_example' # str | 
id = 'id_example' # str | 

try:
    # Update directory instance.
    api_response = api_instance.api_infrastructures_infrastructure_id_directories_id_patch(body, x_api_key, infrastructure_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryApi->api_infrastructures_infrastructure_id_directories_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DirectoriesIdBody**](DirectoriesIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **infrastructure_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**InlineResponse20022**](InlineResponse20022.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

