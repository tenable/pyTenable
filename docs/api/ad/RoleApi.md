# swagger_client.RoleApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_roles_from_from_id_post**](RoleApi.md#api_roles_from_from_id_post) | **POST** /api/roles/from/{fromId} | Creates a new role from another one
[**api_roles_get**](RoleApi.md#api_roles_get) | **GET** /api/roles | Retrieve all role instances.
[**api_roles_id_delete**](RoleApi.md#api_roles_id_delete) | **DELETE** /api/roles/{id} | Delete role instance.
[**api_roles_id_get**](RoleApi.md#api_roles_id_get) | **GET** /api/roles/{id} | Get role instance by id.
[**api_roles_id_patch**](RoleApi.md#api_roles_id_patch) | **PATCH** /api/roles/{id} | Update role instance.
[**api_roles_id_permissions_put**](RoleApi.md#api_roles_id_permissions_put) | **PUT** /api/roles/{id}/permissions | Replace permission list for a role
[**api_roles_post**](RoleApi.md#api_roles_post) | **POST** /api/roles | Create role instance.
[**api_roles_user_creation_defaults_get**](RoleApi.md#api_roles_user_creation_defaults_get) | **GET** /api/roles/user-creation-defaults | Return the default roles for user creation

# **api_roles_from_from_id_post**
> InlineResponse204 api_roles_from_from_id_post(body, x_api_key, from_id)

Creates a new role from another one

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
body = ad.FromFromIdBody1() # FromFromIdBody1 | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
from_id = 'from_id_example' # str | 

try:
    # Creates a new role from another one
    api_response = api_instance.api_roles_from_from_id_post(body, x_api_key, from_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_from_from_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FromFromIdBody1**](FromFromIdBody1.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **from_id** | **str**|  | 

### Return type

[**InlineResponse204**](InlineResponse204.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_get**
> list[InlineResponse20033] api_roles_get(x_api_key)

Retrieve all role instances.

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all role instances.
    api_response = api_instance.api_roles_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20033]**](InlineResponse20033.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_id_delete**
> Object api_roles_id_delete(x_api_key, id)

Delete role instance.

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Delete role instance.
    api_response = api_instance.api_roles_id_delete(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_id_delete: %s\n" % e)
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

# **api_roles_id_get**
> InlineResponse20034 api_roles_id_get(x_api_key, id)

Get role instance by id.

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get role instance by id.
    api_response = api_instance.api_roles_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20034**](InlineResponse20034.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_id_patch**
> InlineResponse20035 api_roles_id_patch(body, x_api_key, id)

Update role instance.

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
body = ad.RolesIdBody() # RolesIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update role instance.
    api_response = api_instance.api_roles_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RolesIdBody**](RolesIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20035**](InlineResponse20035.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_id_permissions_put**
> InlineResponse204 api_roles_id_permissions_put(body, x_api_key, id)

Replace permission list for a role

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
body = [ad.ApirolesPermissions()] # list[ApirolesPermissions] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Replace permission list for a role
    api_response = api_instance.api_roles_id_permissions_put(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_id_permissions_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApirolesPermissions]**](ApirolesPermissions.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse204**](InlineResponse204.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_post**
> list[InlineResponse20033] api_roles_post(body, x_api_key)

Create role instance.

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
body = [ad.ApiRolesBody()] # list[ApiRolesBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create role instance.
    api_response = api_instance.api_roles_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApiRolesBody]**](ApiRolesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20033]**](InlineResponse20033.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_roles_user_creation_defaults_get**
> list[InlineResponse20033] api_roles_user_creation_defaults_get(x_api_key)

Return the default roles for user creation

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
api_instance = ad.RoleApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Return the default roles for user creation
    api_response = api_instance.api_roles_user_creation_defaults_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->api_roles_user_creation_defaults_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20033]**](InlineResponse20033.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

