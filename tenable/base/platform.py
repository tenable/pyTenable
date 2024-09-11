'''
Base Platform
=============

The APIPlatform class is the base class that all platform packages will inherit
from.  Throughout pyTenable v1, packages will be transitioning to using this
base class over the original APISession class.

.. autoclass:: APIPlatform
    :members:
    :inherited-members:
'''
import os
import warnings
import inspect
from restfly import APISession as Base
from tenable.errors import AuthenticationWarning
from tenable.utils import url_validator
from tenable.version import version


class APIPlatform(Base):
    '''
    Base class for all API Platform packages.  This class handles all of the
    base connection logic.

    Args:
        adaptor (Object, optional):
            A Requests Session adaptor to bind to the session object.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  If left
            unspecified, the default is 1 second.
        box (bool, optional):
            Should responses be passed through Box?  If left unspecified, the
            default is ``True``.
        box_attrs (dict, optional):
            Any additional attributes to pass to the Box constructor for this
            session?  For a list of attributes that can be sent, please refer
            to the
            `Box documentation <https://github.com/cdgriffith/Box/wiki>`_
            for more information.
        build (str, optional):
            The build number to put into the User-Agent string.
        product (str, optional):
            The product name to put into the User-Agent string.
        proxies (dict, optional):
            A dictionary detailing what proxy should be used for what
            transport protocol.  This value will be passed to the session
            object after it has been either attached or created.  For
            details on the structure of this dictionary, consult the
            :requests:`proxies <user/advanced/#proxies>` section of the
            Requests documentation.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is 5.
        session (requests.Session, optional):
            Provide a pre-built session instead of creating a requests
            session at instantiation.
        squash_camel (bool, optional):
            Should the responses have CamelCase responses be squashed into
            snake_case?  If left unspecified, the default value is ``False``.
            Note that this will only work when Box is enabled.
        ssl_verify (bool, optional):
            If SSL Verification needs to be disabled (for example when using
            a self-signed certificate), then this parameter should be set to
            ``False`` to disable verification and mask the Certificate
            warnings.
        url (str, optional):
            The base URL that the paths will be appended onto.
        vendor (str, optional):
            The vendor name to put into the User-Agent string.
    '''
    _lib_name = 'pyTenable'
    _lib_version = version
    _backoff = 1
    _retries = 5
    _env_base = ''
    _auth_mech = None
    _allowed_auth_mech_priority = ['key', 'session']
    _allowed_auth_mech_params = {
        'session': ['username', 'password'],
        'key': ['access_key', 'secret_key'],
    }

    def __init__(self, **kwargs):

        # if the constructed URL isn't valid, then we will throw a ConnectionError
        # to inform the caller that something isn't right here.
        url = kwargs.get('url')
        if not url:
            url = os.environ.get(f'{self._env_base}_URL', self._url)
        self._url = url

        if not (self._url and url_validator(self._url, validate=['scheme', 'netloc'])):
            raise ConnectionError(f'{self._url} is not a valid URL')

        # CamelCase squashing is an optional parameter thanks to Box.  if the
        # user has requested it, then we should add the appropriate parameter
        # to the box_attrs.
        if kwargs.get('squash_camel'):
            box_attrs = kwargs.get('box_attrs', {})
            box_attrs['camel_killer_box'] = bool(kwargs.pop('squash_camel'))
            kwargs['box_attrs'] = box_attrs

        # Call the RESTfly constructor
        super().__init__(**kwargs)

    def _session_auth(self, username, password):
        '''
        Default Session auth behavior
        '''
        self.post('session', json={
            'username': username,
            'password': password
        })
        self._auth_mech = 'session'

    def _key_auth(self, access_key, secret_key):
        '''
        Default API Key Auth Behavior
        '''
        self._session.headers.update({
            'X-APIKeys': f'accessKey={access_key}; secretKey={secret_key}'
        })
        self._auth_mech = 'keys'

    def _authenticate(self, **kwargs):
        '''
        This method handles authentication for both API Keys and for session
        authentication.
        '''
        # Here we are grafting the authentication functions into the keyword
        # arguments for later usage.  If a function is provided in the keywords
        # under the key names below, we will use those instead.  This should
        # essentially allow for the authentication logic to be overridden with
        # minimal effort.
        auth = kwargs.get('auth_mechs', {})

        # Collect the auth mechanisms that have been written for this platform.  Auth
        # methods will always end in _auth, so we will simply inspect the platform
        # object and look for any methods that end with '_auth'
        auth_mechs = {
            i[0]: i[1] for i in inspect.getmembers(self, predicate=inspect.ismethod)
            if '_auth' in i[0][-5:]
        }

        # Next we will need to construct the supported auth mechanisms and parameters
        # that were passed into the constructor and store the function and params for
        # each authentication mechanism within the auth dict.
        for name in self._allowed_auth_mech_priority:
            auth[name] = {
                'func': kwargs.get(f'{name}_auth_func', auth_mechs[f'_{name}_auth']),
                'params': {}
            }
            for param in self._allowed_auth_mech_params[name]:
                # for each param, we will attempt to get the value of the parameter,
                # defaulting back to the environment variable as declared with the
                # following syntax:
                # {ENV_BASE}_{PARAM}
                #
                value = kwargs.get(param, None)
                if not value:
                    value = os.getenv(f'{self._env_base}_{param.upper()}', None)

                # If the value is an empty field type, then we will store None instead
                # as we will be using None to denote if all fields were set and if we
                # can use the func for auth.
                if not value:
                    value = None
                auth[name]['params'][param] = value

        # For each authentication mechanism in the priority list, we need to check
        # to see if the all the params have been set.  If all of the parameters have
        # something stored within them, then we will attempt to use this authentication
        # mechanism and return the result of that method back to the caller.
        for name in self._allowed_auth_mech_priority:
            if None not in [v for _, v in auth[name]['params'].items()]:
                return auth[name]['func'](**auth[name]['params'])

        # If we found no valid authentication mechanisms, then we should warn the user
        # that we weren't able to find anything and allow the caller to interact with
        # the unauthenticated session.
        warnings.warn('Starting an unauthenticated session',
                      AuthenticationWarning)
        self._log.warning('Starting an unauthenticated session.')

    def _deauthenticate(self,  # noqa PLW0221
                        method: str = 'DELETE',
                        path: str = 'session'
                        ):
        '''
        This method handles de-authentication.  This is only necessary for
        session-based authentication.
        '''
        if self._auth_mech == 'user':
            self._req(method, path)
        self._auth = {}
        self._auth_mech = None
