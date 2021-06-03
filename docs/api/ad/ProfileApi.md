# swagger_client.ProfileApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_profiles_from_from_id_post**](ProfileApi.md#api_profiles_from_from_id_post) | **POST** /api/profiles/from/{fromId} | Creates a new profile from another one
[**api_profiles_get**](ProfileApi.md#api_profiles_get) | **GET** /api/profiles | Retrieve all profile instances.
[**api_profiles_id_commit_post**](ProfileApi.md#api_profiles_id_commit_post) | **POST** /api/profiles/{id}/commit | Commits change of the related profile
[**api_profiles_id_delete**](ProfileApi.md#api_profiles_id_delete) | **DELETE** /api/profiles/{id} | Delete profile instance.
[**api_profiles_id_get**](ProfileApi.md#api_profiles_id_get) | **GET** /api/profiles/{id} | Get profile instance by id.
[**api_profiles_id_patch**](ProfileApi.md#api_profiles_id_patch) | **PATCH** /api/profiles/{id} | Update profile instance.
[**api_profiles_id_unstage_post**](ProfileApi.md#api_profiles_id_unstage_post) | **POST** /api/profiles/{id}/unstage | Unstages change of the related profile
[**api_profiles_post**](ProfileApi.md#api_profiles_post) | **POST** /api/profiles | Create profile instance.

# **api_profiles_from_from_id_post**
> InlineResponse20031 api_profiles_from_from_id_post(body, x_api_key, from_id)

Creates a new profile from another one

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
body = ad.FromFromIdBody() # FromFromIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
from_id = 'from_id_example' # str | 

try:
    # Creates a new profile from another one
    api_response = api_instance.api_profiles_from_from_id_post(body, x_api_key, from_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_from_from_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FromFromIdBody**](FromFromIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **from_id** | **str**|  | 

### Return type

[**InlineResponse20031**](InlineResponse20031.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_get**
> list[InlineResponse20031] api_profiles_get(x_api_key)

Retrieve all profile instances.

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all profile instances.
    api_response = api_instance.api_profiles_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20031]**](InlineResponse20031.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_id_commit_post**
> Object api_profiles_id_commit_post(x_api_key, id)

Commits change of the related profile

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Commits change of the related profile
    api_response = api_instance.api_profiles_id_commit_post(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_id_commit_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_id_delete**
> Object api_profiles_id_delete(x_api_key, id)

Delete profile instance.

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Delete profile instance.
    api_response = api_instance.api_profiles_id_delete(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_id_get**
> InlineResponse20031 api_profiles_id_get(x_api_key, id)

Get profile instance by id.

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get profile instance by id.
    api_response = api_instance.api_profiles_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20031**](InlineResponse20031.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_id_patch**
> InlineResponse20031 api_profiles_id_patch(body, x_api_key, id)

Update profile instance.

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
body = ad.ProfilesIdBody() # ProfilesIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update profile instance.
    api_response = api_instance.api_profiles_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProfilesIdBody**](ProfilesIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20031**](InlineResponse20031.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_id_unstage_post**
> Object api_profiles_id_unstage_post(x_api_key, id)

Unstages change of the related profile

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Unstages change of the related profile
    api_response = api_instance.api_profiles_id_unstage_post(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_id_unstage_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_profiles_post**
> list[InlineResponse20031] api_profiles_post(body, x_api_key)

Create profile instance.

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
api_instance = ad.ProfileApi(ad.ApiClient(configuration))
body = [ad.ApiProfilesBody()] # list[ApiProfilesBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create profile instance.
    api_response = api_instance.api_profiles_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->api_profiles_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApiProfilesBody]**](ApiProfilesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20031]**](InlineResponse20031.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

