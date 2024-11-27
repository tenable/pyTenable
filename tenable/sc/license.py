'''
License API
===========

The following methods allow for interaction into the Tenable Security Center
:sc-api:`Configuration <Configuration.htm>` API.  These items are typically seen under the
**License Configuration** section of the Tenable Security Center Settings UI.

This API is simple and utilitarian.  No translation of the data returned from the raw API is done.

Methods available on ``sc.license``:

.. rst-class:: hide-signature
.. autoclass:: LicenseAPI
    :members:
'''

from .base import SCEndpoint
from .files import FileAPI

class LicenseAPI(SCEndpoint):
    # def _constructor(self, **kw):
    #     pass
    
    '''
    The way this works is broken for a number of reasons.  The first is that we have to submit the file 
    AND bind the license in one HTTP(S) session.  Otherwise the file gets deleted and the reference to the
    file is lost.  This is why we have to do the file read and upload in a single session in the set() method.
    '''
    def update(self, file):
        '''
        Sets the license file.

        :sc-api:`license: set <license: set>`

        Args:
            file (str): The path to the license file to upload.

        We are using the internal API to do this:
        '''
        # First we need to upload the file.
        filedata = open(file, 'rb')
        
        fAPI = FileAPI(self._api)
        fileName = fAPI.upload(filedata)
        
        filedata.close()
          
        # Now that we have the file uploaded, we can bind the license.
        resp = self._api.post('config/license/register', json={'filename': fileName}).json()
        return resp['response']['config']['LicenseConfig']
    
    def details(self):
        '''
        Retrieves the current license information.

        :sc-api:`license: get <license: get>`

        Returns:
            :obj:`dict`:
                The license information.
        '''
        return self._api.get('configSection/0').json()['response']['LicenseConfig']
