from tenable.base import APISession, APIError, ServerError
from .analysis import SCAnalysisAPI
import warnings


class SecurityCenter(APISession):
    def __init__(self, host, port=443, ssl_verify=False, cert=None,
                 scheme='https', retries=None, backoff=None):
        '''SecurityCenter 5 API Wrapper
        This class is designed to handle authentication management for the
        SecurityCenter 5.x API.  This is by no means a complete model of
        everything that the API can handle, it is simply meant to be a thin
        wrapper into the API.  Convenience functions will be added as time
        passes and there is a desire to develop them.
        For more information, please See Tenable's official API documentation
        at: https://support.tenable.com/support-center/cerberus-support-center/includes/widgets/sc_api/index.html
        '''

        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests) 
        # understands.
        url = '{}://{}:{}/rest'.format(scheme, host, port)

        # Now lets pass the relevent parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        APISession.__init__(self, url, retries, backoff)

        # Also, as SecurityCenter is generally installed without a certificate
        # chain that we can validate, we will want to turn off verification 
        # and the associated warnings unless told to otherwise:
        self._session.verify = ssl_verify
        if not ssl_verify:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

        # If a client-side certificate is specified, then we will want to add
        # it into the session object as well.  The cert parameter is expecting
        # a path pointing to the client certificate file.
        if cert:
            self._session.cert = cert

        # We will attempt to make the first call to the SecurityCenter instance
        # and get the system information.  If this call fails, then we likely
        # aren't pointing to a SecurityCenter at all and should throw an error
        # stating this.
        try:
            d = self.get('system').json()
        except:
            raise ServerError('No SecurityCenter Instance at {}'.format(host))

        # Now we will try to interpret the SecurityCenter information into
        # something usable.
        try:
            self.version = d['response']['version']
            self.build_id = d['response']['buildID']
            self.license = d['response']['licenseStatus']
            self.uuid = d['response']['uuid']
        except:
            raise ServerError('Invalid SecurityCenter Instance')

    def _resp_error_check(self, response):
        try:
            d = response.json()
            if d['error_code']:
                raise APIError(d['error_code'], d['error_msg'])
        except ValueError:
            pass
        return response

    def login(self, user, passwd):
        '''
        Logs the user into SecurityCenter
        Args:
            user (str): Username
            passwd (str): Password
        Returns:
            None
        '''
        resp = self.post('token', json={'username': user, 'password': passwd})
        self._session.headers.update({
            'X-SecurityCenter': str(resp.json()['response']['token'])
        })

    def logout(self):
        '''Logs out of SecurityCenter and removed the cookies and token.'''
        resp = self.delete('token')
        self._build_session()

    def upload(self, fileobj):
        '''
        Uploads a file to SecurityCenter
        Args:
            fileobj (obj): The file object to upload into SecurityCenter.
        '''
        return self.post('file/upload', files={'Filedata': fileobj})

    @property
    def analysis(self):
        '''
        An object for interfacing to the agent exclusions API.  See the
        :doc:`analysis documentation <securitycenter.analysis>` 
        for full details.
        '''
        return SCAnalysisAPI(self)