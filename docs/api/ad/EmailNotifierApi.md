# swagger_client.EmailNotifierApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_email_notifiers_get**](EmailNotifierApi.md#api_email_notifiers_get) | **GET** /api/email-notifiers | Retrieve all email-notifier instances.
[**api_email_notifiers_id_delete**](EmailNotifierApi.md#api_email_notifiers_id_delete) | **DELETE** /api/email-notifiers/{id} | Delete email-notifier instance.
[**api_email_notifiers_id_get**](EmailNotifierApi.md#api_email_notifiers_id_get) | **GET** /api/email-notifiers/{id} | Get email-notifier instance by id.
[**api_email_notifiers_id_patch**](EmailNotifierApi.md#api_email_notifiers_id_patch) | **PATCH** /api/email-notifiers/{id} | Update email-notifier instance.
[**api_email_notifiers_post**](EmailNotifierApi.md#api_email_notifiers_post) | **POST** /api/email-notifiers | Create email-notifier instance.
[**api_email_notifiers_test_message_id_get**](EmailNotifierApi.md#api_email_notifiers_test_message_id_get) | **GET** /api/email-notifiers/test-message/{id} | Send a test email notification by id
[**api_email_notifiers_test_message_post**](EmailNotifierApi.md#api_email_notifiers_test_message_post) | **POST** /api/email-notifiers/test-message | Send a test email notification

# **api_email_notifiers_get**
> list[InlineResponse20023] api_email_notifiers_get(x_api_key)

Retrieve all email-notifier instances.

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Retrieve all email-notifier instances.
    api_response = api_instance.api_email_notifiers_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20023]**](InlineResponse20023.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_email_notifiers_id_delete**
> object api_email_notifiers_id_delete(x_api_key, id)

Delete email-notifier instance.

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Delete email-notifier instance.
    api_response = api_instance.api_email_notifiers_id_delete(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_id_delete: %s\n" % e)
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

# **api_email_notifiers_id_get**
> InlineResponse20023 api_email_notifiers_id_get(x_api_key, id)

Get email-notifier instance by id.

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Get email-notifier instance by id.
    api_response = api_instance.api_email_notifiers_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20023**](InlineResponse20023.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_email_notifiers_id_patch**
> InlineResponse20023 api_email_notifiers_id_patch(body, x_api_key, id)

Update email-notifier instance.

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
body = ad.EmailnotifiersIdBody() # EmailnotifiersIdBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Update email-notifier instance.
    api_response = api_instance.api_email_notifiers_id_patch(body, x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmailnotifiersIdBody**](EmailnotifiersIdBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]
 **id** | **str**|  | 

### Return type

[**InlineResponse20023**](InlineResponse20023.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_email_notifiers_post**
> list[InlineResponse20023] api_email_notifiers_post(body, x_api_key)

Create email-notifier instance.

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
body = [ad.Object()] # list[Object] | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Create email-notifier instance.
    api_response = api_instance.api_email_notifiers_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[Object]**](Object.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**list[InlineResponse20023]**](InlineResponse20023.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_email_notifiers_test_message_id_get**
> Object api_email_notifiers_test_message_id_get(x_api_key, id)

Send a test email notification by id

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)
id = 'id_example' # str | 

try:
    # Send a test email notification by id
    api_response = api_instance.api_email_notifiers_test_message_id_get(x_api_key, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_test_message_id_get: %s\n" % e)
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

# **api_email_notifiers_test_message_post**
> Object api_email_notifiers_test_message_post(body, x_api_key)

Send a test email notification

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
api_instance = ad.EmailNotifierApi(ad.ApiClient(configuration))
body = ad.EmailnotifiersTestmessageBody() # EmailnotifiersTestmessageBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Send a test email notification
    api_response = api_instance.api_email_notifiers_test_message_post(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailNotifierApi->api_email_notifiers_test_message_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmailnotifiersTestmessageBody**](EmailnotifiersTestmessageBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**Object**](Object.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

