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
from restfly import APISession as Base
from tenable.utils import url_validator
from tenable.version import version
import os, warnings


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
            defaut is ``True``.
        box_attrs (dict, optional):
            Any additional attributes to pass to the Box constructor for this
            session?  For a list of attributes that can be sent, please refer
            to the `Box documentation <https://github.com/cdgriffith/Box/wiki>`_
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
    _box = True
    _backoff = 1
    _retries = 5
    _env_base = ''
    _port = 443
    _scheme = 'https'
    _address = None
    _auth = (None, None)
    _auth_mech = None
    _box_attrs = dict()

    def __init__(self, **kwargs):
        # Constructing the URL from the various parameters.
        self._url = '{}://{}:{}'.format(
            kwargs.get('scheme', self._scheme),
            kwargs.get('address', os.getenv(
                '{}_ADDRESS'.format(self._env_base), self._address)),
            kwargs.get('port', os.getenv(
                '{}_PORT'.format(self._env_base), self._port)),
        )

        # if the constructed URL isn't valid, then we will throw a TypeError
        # to inform the caller that something isn't right here.
        if not url_validator(self._url):
            raise TypeError('{url} is not a valid URL'.format(url=self._url))

        # CamelCase squashing is an optional parameter thanks to Box.  if the
        # user has requested it, then we should add the appropriate parameter to
        # the box_attrs.
        if kwargs.get('squash_camel'):
            box_attrs = kwargs.get('box_attrs', {})
            box_attrs['camel_killer_box'] = bool(kwargs.pop('squash_camel'))
            kwargs['box_attrs'] = box_attrs

        # Call the RESTfly constructor
        super(APIPlatform, self).__init__(**kwargs)

    def _authenticate(self, **kwargs):
        '''
        This method handles authentication for both API Keys and for session
        authentication.
        '''

        # These functions determine how authentication is to be handled within
        # for both session authentication and key-based authentication.  They
        # have been broken down into these functions for easy overloading.
        def key_auth():
            '''
            Default API Key Auth Behavior
            '''
            self._session.headers.update({
                'X-APIKeys': 'accessKey={}; secretKey={}'.format(*keys)
            })
            self._auth_mech = 'keys'

        def s_auth():
            '''
            Default Session auth behavior
            '''
            self.post('session', json={
                'username': self._auth[0],
                'password': self._auth[1]
            })
            self._auth_mech = 'user'

        # Here we are grafting the authentication functions into the keyword
        # arguments for later usage.  If a function is provided in the keywords
        # under the key names below, we will use those instead.  This should
        # essentially allow for the authentication logic to be overridden with
        # minimal effort.
        kwargs['key_auth_func'] = kwargs.get('key_auth_func', key_auth)
        kwargs['session_auth_func'] = kwargs.get('session_auth_func', s_auth)

        # Pull the API keys from the keyword arguments passed to the constructor
        # and build the keys tuple.  As API Keys will be injected directly into
        # the session, there is no need to store these.
        keys = (
            kwargs.get('access_key', os.getenv(
                '{}_ACCESS_KEY'.format(self._env_base))),
            kwargs.get('secret_key', os.getenv(
                '{}_SECRET_KEY'.format(self._env_base)))
        )

        # The session authentication tuple.  We will be storing these as its
        # possible for the session to timeout on the user.  This would require
        # re-authentication.
        self._auth = (
            kwargs.get('username', os.getenv(
                '{}_USERNAME'.format(self._env_base))),
            kwargs.get('password', os.getenv(
                '{}_PASSWORD'.format(self._env_base)))
        )

        # Run the desired authentication function.  As API keys are generally
        # preferred over session authentication, we will first check to see that
        # keys have been
        if None not in keys:
            kwargs['key_auth_func']()
        elif None not in self._auth:
            kwargs['session_auth_func']()
        else:
            warnings.warn('Starting an unauthenticated session')
            self._log.warning('Starting an unauthenticated session.')

    def _deauthenticate(self):
        '''
        This method handles de-authentication.  This is only necessary for
        session-based authentication.
        '''
        if self._auth_mech == 'user':
            self.delete('session')
        self._auth = (None, None)
        self._auth_mech = None