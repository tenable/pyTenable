from tenable.base import APIEndpoint

class ScansAPI(APIEndpoint):
    def __init__(self, api):
        APIEndpoint.__init__(self, api)

        # Now lets graft on Scan Endpoints

    def timezones(self):
        '''
        `scans: timezones <https://cloud.tenable.com/api#/resources/scans/timezones>`_

        Returns:
            list: List of allowed timezone strings accepted by Tenable.IO
        '''
        resp = self._api.get('scans/timezones').json()['timezones']
        return [i['value'] for i in resp]