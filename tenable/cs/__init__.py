'''
Documentation pending rewrite of the ContainerSecurity package to take advantage
of the v2 APIs.
'''
from tenable.base import APISession
from .compliance import ComplianceAPI
from .containers import ContainersAPI
from .imports import ImportAPI
from .jobs import JobsAPI
from .registry import RegistryAPI
from .reports import ReportsAPI
from .uploads import UploadAPI

class ContainerSecurity(APISession):
    '''
    The Container Security object is the primary interaction point for users to
    interface with Container Security via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Tenable.io.
        secret_key (str):
            The user's API secret key for Tenable.io.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com``.
        registry (str, optional): 
            The registry path to use for docker pushes.  The default is
            ``registry.cloud.tenable.com``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``0.1`` seconds.
    '''
    _url = 'https://cloud.tenable.com/container-security/api'
    _registry = 'registry.cloud.tenable.com'

    @property
    def compliance(self):
        '''
        An object for interfacing to the image compliance API.  See the
        :doc:`compliance documentation <cs.compliance>` 
        for full details.
        '''
        return ComplianceAPI(self)

    @property
    def containers(self):
        '''
        An object for interfacing to the containers API.  See the
        :doc:`containers documentation <cs.containers>` 
        for full details.
        '''
        return ContainersAPI(self)

    @property
    def imports(self):
        '''
        An object for interfacing to the imports API.  See the
        :doc:`imports documentation <cs.imports>` 
        for full details.
        '''
        return ImportAPI(self)

    @property
    def jobs(self):
        '''
        An object for interfacing to the jobs API.  See the
        :doc:`jobs documentation <cs.jobs>` 
        for full details.
        '''
        return JobsAPI(self)

    @property
    def registry(self):
        '''
        An object for interfacing to the image registry API.  See the
        :doc:`registry documentation <cs.registry>` 
        for full details.
        '''
        return RegistryAPI(self)

    @property
    def reports(self):
        '''
        An object for interfacing to the image reports API.  See the
        :doc:`reports documentation <cs.reports>` 
        for full details.
        '''
        return ReportsAPI(self)

    @property
    def uploads(self):
        '''
        An object for interfacing to the image uploading API.  See the
        :doc:`uploads documentation <cs.uploads>` 
        for full details.
        '''
        return UploadAPI(self)

    def __init__(self, access_key, secret_key, 
                 url=None, retries=None, backoff=None, registry=None):
        self._access_key = access_key
        self._secret_key = secret_key
        if registry:
            self._registry = registry
        APISession.__init__(self, url, retries, backoff)

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
    
    
    
    
    