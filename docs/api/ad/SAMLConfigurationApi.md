# swagger_client.SAMLConfigurationApi

All URIs are relative to *{protocol}://customer.alsid.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_saml_configuration_generate_certificate_get**](SAMLConfigurationApi.md#api_saml_configuration_generate_certificate_get) | **GET** /api/saml-configuration/generate-certificate | Generates SAML certificate
[**api_saml_configuration_get**](SAMLConfigurationApi.md#api_saml_configuration_get) | **GET** /api/saml-configuration | Get saml-configuration singleton.
[**api_saml_configuration_patch**](SAMLConfigurationApi.md#api_saml_configuration_patch) | **PATCH** /api/saml-configuration | Update saml-configuration singleton.

# **api_saml_configuration_generate_certificate_get**
> InlineResponse20037 api_saml_configuration_generate_certificate_get(x_api_key)

Generates SAML certificate

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
api_instance = ad.SAMLConfigurationApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Generates SAML certificate
    api_response = api_instance.api_saml_configuration_generate_certificate_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SAMLConfigurationApi->api_saml_configuration_generate_certificate_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20037**](InlineResponse20037.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_saml_configuration_get**
> InlineResponse20036 api_saml_configuration_get(x_api_key)

Get saml-configuration singleton.

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
api_instance = ad.SAMLConfigurationApi(ad.ApiClient(configuration))
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Get saml-configuration singleton.
    api_response = api_instance.api_saml_configuration_get(x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SAMLConfigurationApi->api_saml_configuration_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_saml_configuration_patch**
> InlineResponse20036 api_saml_configuration_patch(body, x_api_key)

Update saml-configuration singleton.

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
api_instance = ad.SAMLConfigurationApi(ad.ApiClient(configuration))
body = ad.ApiSamlconfigurationBody() # ApiSamlconfigurationBody | 
x_api_key = 'put-your-api-key-here' # str | The user's API key (default to put-your-api-key-here)

try:
    # Update saml-configuration singleton.
    api_response = api_instance.api_saml_configuration_patch(body, x_api_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SAMLConfigurationApi->api_saml_configuration_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiSamlconfigurationBody**](ApiSamlconfigurationBody.md)|  | 
 **x_api_key** | **str**| The user&#x27;s API key | [default to put-your-api-key-here]

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

