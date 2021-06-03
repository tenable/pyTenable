# swagger_client.UserApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_login_post**](UserApi.md#api_login_post) | **POST** /api/login | Logs in a user
[**api_logout_post**](UserApi.md#api_logout_post) | **POST** /api/logout | Logs out a user
[**api_users_forgotten_password_post**](UserApi.md#api_users_forgotten_password_post) | **POST** /api/users/forgotten-password | Sends an email to create a new password
[**api_users_get**](UserApi.md#api_users_get) | **GET** /api/users | Get all users
[**api_users_id_delete**](UserApi.md#api_users_id_delete) | **DELETE** /api/users/{id} | Delete user instance.
[**api_users_id_get**](UserApi.md#api_users_id_get) | **GET** /api/users/{id} | Get user instance by id.
[**api_users_id_patch**](UserApi.md#api_users_id_patch) | **PATCH** /api/users/{id} | Update user instance.
[**api_users_id_roles_put**](UserApi.md#api_users_id_roles_put) | **PUT** /api/users/{id}/roles | Replace role list for a user
[**api_users_password_patch**](UserApi.md#api_users_password_patch) | **PATCH** /api/users/password | Update a user&#x27;s password
[**api_users_post**](UserApi.md#api_users_post) | **POST** /api/users | Create user instance.
[**api_users_retrieve_password_post**](UserApi.md#api_users_retrieve_password_post) | **POST** /api/users/retrieve-password | Retrieves a user&#x27;s password
[**api_users_whoami_get**](UserApi.md#api_users_whoami_get) | **GET** /api/users/whoami | Get a user&#x27;s information

# **api_login_post**
> InlineResponse20044 api_login_post(body)

Logs in a user

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ad.UserApi()
body = ad.ApiLoginBody() # ApiLoginBody | 

try:
    # Logs in a user
    api_response = api_instance.api_login_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_login_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiLoginBody**](ApiLoginBody.md)|  | 

### Return type

[**InlineResponse20044**](InlineResponse20044.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_logout_post**
> str api_logout_post(x_api_key)

Logs out a user

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Logs out a user
    api_response = api_instance.api_logout_post(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_logout_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_forgotten_password_post**
> Object api_users_forgotten_password_post(body)

Sends an email to create a new password

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ad.UserApi()
body = ad.UsersForgottenpasswordBody() # UsersForgottenpasswordBody | 

try:
    # Sends an email to create a new password
    api_response = api_instance.api_users_forgotten_password_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_forgotten_password_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UsersForgottenpasswordBody**](UsersForgottenpasswordBody.md)|  | 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_get**
> list[InlineResponse20041] api_users_get(x_api_key)

Get all users

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get all users
    api_response = api_instance.api_users_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20041]**](InlineResponse20041.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_id_delete**
> object api_users_id_delete(x_api_key, id)

Delete user instance.

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Delete user instance.
    api_response = api_instance.api_users_id_delete(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_id_delete: %s\n" % e)
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

# **api_users_id_get**
> InlineResponse20043 api_users_id_get(x_api_key, id)

Get user instance by id.

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get user instance by id.
    api_response = api_instance.api_users_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20043**](InlineResponse20043.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_id_patch**
> InlineResponse20041 api_users_id_patch(body, x_api_key, id)

Update user instance.

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
body = ad.UsersIdBody() # UsersIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update user instance.
    api_response = api_instance.api_users_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UsersIdBody**](UsersIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20041**](InlineResponse20041.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_id_roles_put**
> InlineResponse20045 api_users_id_roles_put(body, x_api_key, id)

Replace role list for a user

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
body = ad.IdRolesBody() # IdRolesBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Replace role list for a user
    api_response = api_instance.api_users_id_roles_put(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_id_roles_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**IdRolesBody**](IdRolesBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20045**](InlineResponse20045.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_password_patch**
> Object api_users_password_patch(body, x_api_key)

Update a user's password

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
body = ad.UsersPasswordBody() # UsersPasswordBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update a user's password
    api_response = api_instance.api_users_password_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_password_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UsersPasswordBody**](UsersPasswordBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_post**
> list[InlineResponse20041] api_users_post(body, x_api_key)

Create user instance.

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
body = [ad.ApiUsersBody()] # list[ApiUsersBody] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create user instance.
    api_response = api_instance.api_users_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[ApiUsersBody]**](ApiUsersBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20041]**](InlineResponse20041.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_retrieve_password_post**
> Object api_users_retrieve_password_post(body)

Retrieves a user's password

### Example

```python
from __future__ import print_function
import time
import ad
from ad.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ad.UserApi()
body = ad.UsersRetrievepasswordBody() # UsersRetrievepasswordBody | 

try:
    # Retrieves a user's password
    api_response = api_instance.api_users_retrieve_password_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_retrieve_password_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UsersRetrievepasswordBody**](UsersRetrievepasswordBody.md)|  | 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_users_whoami_get**
> InlineResponse20042 api_users_whoami_get(x_api_key)

Get a user's information

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
api_instance = ad.UserApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get a user's information
    api_response = api_instance.api_users_whoami_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->api_users_whoami_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20042**](InlineResponse20042.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

