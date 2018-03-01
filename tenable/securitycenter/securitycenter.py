from tenable.base import APISession, APIError, ServerError
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

    def analysis(self, *filters, **kwargs):
        '''Analysis
        A thin wrapper to handle vuln/event/mobile/log analysis through the API.
        This function handles expanding multiple filters and will translate 
        arbitrary arguments into the format that SecurityCenter's analysis call
        expect them to be in.

        In order to make the filter expander more useful for SecurityCenter5
        verses the SecurityCenter4 class, filters are no longer done as kwargs,
        and instead are done as a list of tuples.  For example, to get the IP 
        Summary of all of the hosts in the 10.10.0.0/16 network, we would make
        the following call:

        vulns = sc.analysis(('ip','=','10.10.0.0/16'), tool='sumip')

        If multiple filters are desired, then it's simply a matter of entering
        multiple tuples.

        The Analysis function also has a few functions that are sligly deviated
        from the API guides.  All of these options are optional, however can
        significantly change the how the API is being called.

        https://docs.tenable.com/sccv/api/Analysis.html

        Args:
            filters (tuple, optional):
                The analysis module provides a more compact way to write filters
                to the analysis endpoint.  The purpose here is to aid in more
                readable code and reduce the amount of boilerplate that must be
                written to support a filtered call to analysis.  The format is
                simply a list of tuples.  Each tuple is broken down into
                (field, operator, value).
            page (int, optional): 
                The current page in the pagination sequence.  Default is `all`.
            page_size (int, optional): 
                The page size (number of returned results).  Default is 1000.
            func (func, optional):
                Overload the default behavior and use the provided function 
                instead.
            func_kw (dict, optional): 
                If arguments need to be passed to the provided page_func, then
                provide them as a keyword dictionary.
            type (str, optional):
                The type of data that we desire to query against.  While the
                default is to look at vulnerability data with the 'vuln' type,
                it's possible you may want to look at event data from the LCE or
                mobile device data from an MDM repository.  If this is the case,
                simply overload the type with the expected data to be returned.
                Available types are: ``vuln``, ``event``, ``user``, ``scLog``, 
                ``mobile``.
            sourceType (str, optional):
                Change the type of data within the source to be queried.  The
                default is to look at the cumulative data-store with the
                sourceType set to 'cumulative'.  Available sourceTypes are:
                ``individual``, ``cumulative``, ``patched``, ``lce``, 
                ``archive``.
            sortDir (str, optional):
                The sorting direction for the sortField.  Must be `ASC` 
                or `DESC`.
            sortField (str, optional):
                The field to sort the results on.  Any valid field returned by
                the results can be sorted.
            scanID (int, optional):
                If the sourceType is set to ``individual``, then a Scan ID must 
                be specified to inform SecurityCenter what scan to query against.
            lceID (int, optional):
                If the sourceType is ``lce`` or ``archive``, then an lceID can 
                be specified to explicitly define 1 LCE to query from.
            view (string, optional):
                If the sourceType is ``archive``, then the archived Silo ID must
                be specified in order to inform the LCE which silo to query.
            tool (string, optional):
                The analysis tool to use for parsing the data.  Available
                tool types are as follows:
                
                * ``vuln`` DataType Tools:
                    ``cceipdetail``, ``cveipdetail``, ``iavmipdetail``, 
                    ``iplist``, ``listmailclients``, ``listservices``, 
                    ``listos``, ``listsoftware``, ``listsshservers``,
                    ``listvuln``, ``listwebclients``, ``listwebservers``,
                    ``popcount``, ``sumasset``, ``sumcce``, ``sumclassa``,
                    ``sumclassb``, ``sumclassc``, ``sumcve``, ``sumdnsname``,
                    ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,
                    ``summsbulletin``, ``sumprotocol``, ``sumremediation``,
                    ``sumseverity``, ``sumuserresponsibility``, ``support``,
                    ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``
                * ``event`` DataType Tools:
                    ``listdata``, ``sumasset``, ``sumclassa``, ``sumclassb``,
                    ``sumclassc``, ``sumconns``, ``sumdate``, ``sumdstip``,
                    ``sumevent``, ``sumevent2``, ``sumip``, ``sumport``,
                    ``sumprotocol``, ``sumsrcip``, ``sumtime``, ``sumtype``,
                    ``sumuser``, ``syslog``, ``timedist``
                * ``mobile`` DataType Tools:
                    ``listmodel``, ``listoscpe``, ``listvuln``, ``sumdeviceid``,
                    ``summdmuser``, ``summodel``, ``sumoscpe``, ``sumpluginid``,
                    ``sumprotocol``, ``sumseverity``, ``support``, ``vulndetails``
        '''
        output = []
        def return_results(**kw):
            return kw['resp']['response']['results']

        def return_generator(**kw):
            for item in kw['resp']['response']['results']:
                yield item

        # These values are commonly used and/or are generally not changed from 
        # the default. If we do not see them specified by the user then we will
        # need to add these in for later parsing...
        if 'page' not in kwargs: kwargs['page'] = 'all'
        if 'page_size' not in kwargs: kwargs['page_size'] = 1000
        if 'func' not in kwargs: kwargs['func'] = return_results
        if 'func_kw' not in kwargs: kwargs['func_kw'] = {}
        if 'type' not in kwargs: kwargs['type'] = 'vuln'
        if 'sourceType' not in kwargs: kwargs['sourceType'] = 'cumulative'
        if 'generator' in kwargs: kwargs['generator'] = return_generator

        # New we need to pull out the options from kwargs as we will be using 
        # kwargs as the basis for the query that will be sent to SecurityCenter.
        opts = {}
        for opt in ['page', 'page_size', 'func', 'func_kw', 'generator']:
            if opt in kwargs:
                opts[opt] = kwargs[opt]
                del kwargs[opt]

        # If a query option was not set, then we will have to.  The hope here is
        # that we can make a lot of the pain of building the query pretty easy 
        # by simply accepting tuples of the filters.
        if 'query' not in kwargs:
            kwargs['query'] = {
                'tool': kwargs['tool'],
                'type': kwargs['type'],
                'filters': [{
                    'filterName': f[0], 
                    'operator': f[1], 
                    'value': f[2], 
                    'type': kwargs['type']
                } for f in filters]
            }
            del kwargs['tool']
            if opts['page'] == 'all':
                kwargs['query']['startOffset'] = 0
                kwargs['query']['endOffset'] = opts['page_size']
            else:
                kwargs['query']['startOffset'] = opts['page'] * opts['page_size']
                kwargs['query']['endOffset'] = (opts['page'] + 1) * opts['page_size']

        count = 0
        total_records = opts['page_size']
        while total_records > count:
            # Here we actually make the calls.
            resp = self.post('analysis', json=kwargs).json()
            opts['func_kw']['resp'] = resp
            out = opts['func'](**opts['func_kw'])
            if isinstance(out, list):
                for item in out:
                    output.append(item)
            total_records = int(resp.json()['response']['totalRecords'])
            if opts['page'] == 'all':
                count = int(resp.json()['response']['endOffset'])
                kwargs['query']['startOffset'] = count
                kwargs['query']['endOffset'] = count + opts['page_size']
            else:
                count = total_records
        if len(output) > 0:
            return output
