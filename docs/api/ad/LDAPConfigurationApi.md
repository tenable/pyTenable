# swagger_client.LDAPConfigurationApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_ldap_configuration_get**](LDAPConfigurationApi.md#api_ldap_configuration_get) | **GET** /api/ldap-configuration | Get ldap-configuration singleton.
[**api_ldap_configuration_patch**](LDAPConfigurationApi.md#api_ldap_configuration_patch) | **PATCH** /api/ldap-configuration | Update ldap-configuration singleton.

# **api_ldap_configuration_get**
> InlineResponse20028 api_ldap_configuration_get(x_api_key)

Get ldap-configuration singleton.

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
api_instance = ad.LDAPConfigurationApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get ldap-configuration singleton.
    api_response = api_instance.api_ldap_configuration_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LDAPConfigurationApi->api_ldap_configuration_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20028**](InlineResponse20028.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_ldap_configuration_patch**
> InlineResponse20028 api_ldap_configuration_patch(body, x_api_key)

Update ldap-configuration singleton.

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
api_instance = ad.LDAPConfigurationApi(ad.ApiClient(configuration))
body = ad.ApiLdapconfigurationBody() # ApiLdapconfigurationBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update ldap-configuration singleton.
    api_response = api_instance.api_ldap_configuration_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LDAPConfigurationApi->api_ldap_configuration_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiLdapconfigurationBody**](ApiLdapconfigurationBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20028**](InlineResponse20028.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

