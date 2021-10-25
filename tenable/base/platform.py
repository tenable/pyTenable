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
    _auth = {}
    _auth_mech = None

    def __init__(self, **kwargs):

        # if the constructed URL isn't valid, then we will throw a TypeError
        # to inform the caller that something isn't right here.
        self._url = kwargs.get('url',
                               os.environ.get(f'{self._env_base}_URL',
                                              self._url
                                              )
                               )
        if not url_validator(self._url):
            raise TypeError(f'{self._url} is not a valid URL')

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
        self._auth_mech = 'user'

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
        kwargs['key_auth_func'] = kwargs.get('key_auth_func',
                                             self._key_auth)
        kwargs['session_auth_func'] = kwargs.get('session_auth_func',
                                                 self._session_auth)

        # Pull the API keys from the keyword arguments passed to the
        # constructor and build the keys tuple.  As API Keys will be
        # injected directly into the session, there is no need to store these.
        keys = kwargs.get('_key_auth_dict', {
            'access_key': kwargs.get('access_key',
                                     os.getenv(f'{self._env_base}_ACCESS_KEY')
                                     ),
            'secret_key': kwargs.get('secret_key',
                                     os.getenv(f'{self._env_base}_SECRET_KEY')
                                     )
        })

        # The session authentication tuple.  We will be storing these as its
        # possible for the session to timeout on the user.  This would require
        # re-authentication.
        self._auth = kwargs.get('_session_auth_dict', {
            'username': kwargs.get('username',
                                   os.getenv(f'{self._env_base}_USERNAME')
                                   ),
            'password': kwargs.get('password',
                                   os.getenv(f'{self._env_base}_PASSWORD')
                                   )
        })

        # Run the desired authentication function.  As API keys are generally
        # preferred over session authentication, we will first check to see
        # that keys have been set, as we prefer stateless auth to stateful.
        if None not in [v for _, v in keys.items()]:
            kwargs['key_auth_func'](**keys)
        elif None not in [v for _, v in self._auth.items()]:
            kwargs['session_auth_func'](**self._auth)
        else:
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
