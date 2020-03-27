'''
audit_files
===========

The following methods allow for interaction into the Tenable.sc
:sc-api:`Audit File <AuditFile.html>` API and the
:sc-api:`Audit File Template <AuditFile-Template.html>` API.  These items are
typically seen under the **Scans: Audit Files** section of Tenable.sc.

Methods available on ``sc.audit_files``:

.. rst-class:: hide-signature
.. autoclass:: AuditFileAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: template_categories
    .. automethod:: template_details
    .. automethod:: template_list
'''
from .base import SCEndpoint
from io import BytesIO
from os.path import basename

class AuditFileAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a audit file definition document
        '''
        if 'name' in kw:
            # Validate that the name parameter is a string.
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # Validate that the description parameter is a string,
            self._check('description', kw['description'], str)

        if 'type' in kw:
            # Validate that the type is one of the 3 possible audit file types:
            # "", "scapWindows", or "scapLinux".
            self._check('type', kw['type'], str,
                choices=['', 'scapWindows', 'scapLinux'])

        if 'template' in kw:
            # Convert the template parameter into the auditFileTemplate
            # sub-document and verify that the input is an integer value.
            kw['auditFileTemplate'] = {'id': self._check(
                'template', kw['template'], int)}
            del(kw['template'])

        if 'vars' in kw:
            # expand the the vars dict into a series of key/value documents.
            kw['variables'] = [{
                    'name': self._check('var:name', k, str),
                    'value': self._check('var:value', v, str)
                } for k,v in self._check('vars', kw['vars'], dict).items()]
            del(kw['vars'])

        if 'filename' in kw:
            # Validate that the filename parameter is a string.
            self._check('filename', kw['filename'], str)

        if 'orig_filename' in kw:
            # validate the the original_filename parameter is of type string and
            # then store it in the CamelCase equiv:
            kw['originalFilename'] = self._check(
                'orig_filename', kw['orig_filename'], str)
            del(kw['orig_filename'])

        if 'version' in kw:
            # Validate that the version parameter is of type string and falls
            # within the expected range of values
            self._check('version', kw['version'], str,
                choices=['1.0', '1.1', '1.2'])

        if 'benchmark' in kw:
            # Validate that the benchmark name is a string and then store it
            # in the benchmarkName attribute.
            kw['benchmarkName'] = self._check('benchmark', kw['benchmark'], str)
            del(kw['benchmark'])

        if 'profile' in kw:
            # Validate that the profile name is a string and then store it in
            # the profileName attribute.
            kw['profileName'] = self._check('profile', kw['profile'], str)
            del(kw['profile'])

        if 'data_stream' in kw:
            # Validate that the profile_stream attribute is a string and then
            # store it in the dataStreamName attribute.
            kw['dataStreamName'] = self._check(
                'data_stream', kw['data_stream'], str)
            del(kw['data_stream'])

        if 'tailoring_filename' in kw:
            kw['tailoringFilename'] = self._check(
                'tailoring_filename', kw['tailoring_filename'], str)
            del(kw['tailoring_filename'])

        if 'tailoring_orig_filename' in kw:
            kw['tailoringOriginalFilename'] = self._check(
                'tailoring_orig_filename', kw['tailoring_orig_filename'], str)
            del(kw['tailoring_orig_filename'])

        return kw

    def create(self, name, audit_file=None, tailoring_file=None, **kw):
        '''
        Creates a audit file.

        :sc-api:`audit file: create <AuditFile.html#auditFile_POST>`

        Args:
            name (str):
                The name of the audit file.
            audit_file (FileObject, optional):
                The file-like object containing the audit file if uploading a
                custom audit file.
            benchmark (str, optional):
                When the type is set to either SCAP datatype, this specifies the
                name of the benchmark.
            data_stream (str, optional):
                When using version 1.2 of either SCAP datatype, you must specify
                the name of the data stream.
            description (str, optional):
                A description of for the audit file.
            profile (str, optional):
                When the type is set to either SCAP datatype, this specifies the
                name of the profile.
            tailoring_file (FileObject, optional):
                When the SCAP version is set to 1.2, this tailoring file can
                optionally be provided.
            template (int, optional):
                The audit file template it to use.  If using a template, then no
                file is uploaded.
            type (str, optional):
                The type of audit file to upload.  Generally only used when
                uploading SCAP content as it will default to the Tenable-created
                audit-file format.  Supported SCAP values are ``scapWindows``
                and ``scapLinux``.
            vars (dict, optional):
                If a template is specified, then this dictionary specifies the
                parameters within the template to customize and what those
                values should be.  The values are provided within the template
                definition.
            version (str, optional):
                When specifying a SCAP datatype, this informs Tenable.sc what
                version of SCAP this audit checklist is.  Supported values are
                ``1.0``, ``1.1``, and ``1.2``.

        Returns:
            :obj:`dict`:
                The newly created audit file.

        Examples:
            >>> audit = sc.audit_files.create()
        '''
        kw['name'] = name

        # Upload and store the relevent information on the audit file that has
        # been provided.
        if audit_file:
            if hasattr(audit_file, 'name'):
                kw['orig_filename'] = basename(audit_file.name)
            kw['filename'] = self._api.files.upload(audit_file)

        # Upload and store the relevent information on the tailoring file that
        # has been provided.
        if tailoring_file:
            if hasattr(tailoring_file, 'name'):
                kw['tailoring_orig_filename'] = basename(tailoring_file.name)
            kw['tailoring_filename'] = self._api.files.upload(tailoring_file)

        payload = self._constructor(**kw)
        return self._api.post('auditFile', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific audit file.

        :sc-api:`audit file: details <AuditFile.html#AuditFileRESTReference-/auditFile/{id}>`

        Args:
            id (int): The identifier for the audit file.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The audit file resource record.

        Examples:
            >>> audit = sc.audit_files.details(1)
            >>> pprint(audit)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('auditFile/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, audit_file=None, tailoring_file=None, **kw):
        '''
        Edits a audit file.

        :sc-api:`audit file: edit <AuditFile.html#auditFile_id_PATCH>`

        Args:
            audit_file (FileObject, optional):
                The file-like object containing the audit file if uploading a
                custom audit file.
            benchmark (str, optional):
                When the type is set to either SCAP datatype, this specifies the
                name of the benchmark.
            data_stream (str, optional):
                When using version 1.2 of either SCAP datatype, you must specify
                the name of the data stream.
            description (str, optional):
                A description of for the audit file.
            name (str, optional):
                The name of the audit file.
            profile (str, optional):
                When the type is set to either SCAP datatype, this specifies the
                name of the profile.
            tailoring_file (FileObject, optional):
                When the SCAP version is set to 1.2, this tailoring file can
                optionally be provided.
            template (int, optional):
                The audit file template it to use.  If using a template, then no
                file is uploaded.
            type (str, optional):
                The type of audit file to upload.  Generally only used when
                uploading SCAP content as it will default to the Tenable-created
                audit-file format.  Supported SCAP values are ``scapWindows``
                and ``scapLinux``.
            vars (dict, optional):
                If a template is specified, then this dictionary specifies the
                parameters within the template to customize and what those
                values should be.  The values are provided within the template
                definition.
            version (str, optional):
                When specifying a SCAP datatype, this informs Tenable.sc what
                version of SCAP this audit checklist is.  Supported values are
                ``1.0``, ``1.1``, and ``1.2``.

        Returns:
            :obj:`dict`:
                The newly updated audit file.

        Examples:
            >>> audit = sc.audit_files.edit()
        '''

        # Upload and store the relevent information on the audit file that has
        # been provided.
        if audit_file:
            if hasattr(audit_file, 'name'):
                kw['orig_filename'] = basename(audit_file.name)
            kw['filename'] = self._api.files.upload(audit_file)

        # Upload and store the relevent information on the tailoring file that
        # has been provided.
        if tailoring_file:
            if hasattr(tailoring_file, 'name'):
                kw['tailoring_orig_filename'] = basename(tailoring_file.name)
            kw['tailoring_filename'] = self._api.files.upload(tailoring_file)

        payload = self._constructor(**kw)
        return self._api.patch('auditFile/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a audit file.

        :sc-api:`audit file: delete <AuditFile.html#auditFile_id_DELETE>`

        Args:
            id (int): The numeric identifier for the audit file to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.audit_files.delete(1)
        '''
        return self._api.delete('auditFile/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        :sc-api:`audit file: list <AuditFile.html#AuditFileRESTReference-/auditFile>`

        Args:
            fields (list, optional):
                A list of attributes to return for each audit file.

        Returns:
            :obj:`list`:
                A list of audit file resources.

        Examples:
            >>> for audit in sc.audit_files.list():
            ...     pprint(audit)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('auditFile', params=params).json()['response']

    def export_audit(self, id, fobj=None):
        '''
        Exports an Audit File.

        :sc-api:`audit file: export <AuditFile.html#AuditFileRESTReference-/auditFile/{id}/export>`

        Args:
            id (int): The audit file numeric identifier.
            fobj (FileObject, optional):
                The file-like object to write the resulting file into.  If
                no file-like object is provided, a BytesIO objects with the
                downloaded file will be returned.  Be aware that the default
                option of using a BytesIO object means that the file will be
                stored in memory, and it's generally recommended to pass an
                actual file-object to write to instead.

        Returns:
            :obj:`FileObject`:
                The file-like object with the resulting zipped report.

        Examples:
            >>> with open('example.zip', 'wb') as fobj:
            ...     sc.audit_files.export_audit(1, fobj)
        '''
        resp = self._api.get('auditFile/{}/export'.format(
            self._check('id', id, int)), stream=True)

        # if no file-like object was passed, then we will instantiate a BytesIO
        # object to push the file into.
        if not fobj:
            fobj = BytesIO()

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def template_categories(self):
        '''
        Returns the audit file template categories

        :sc-api:`audit template: categories <AuditFile-Template.html#auditFileTemplate_categories_GET>`

        Returns:
            :obj:`list`:
                List of audit file category listing dicts.

        Exmaples:
            >>> for cat in sc.audit_files.template_categorties():
            ...     pprint(cat)
        '''
        return self._api.get('auditFileTemplate/categories').json()['response']

    def template_details(self, id, fields=None):
        '''
        Returns the details for the specified audit file template id.

        :sc-api:`audit template: details <AuditFile-Template.html#auditFileTemplate_id_GET>`

        Args:
            id (int):
                The numeric identifier for the audit file template.
            fields (list, optional):
                A list of attributes to return.

        Returns:
            :obj:`dict`:
                The audit file template record.

        Exmaples:
            >>> tmpl = sc.audit_files.template_details(1)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('auditFileTemplate/{}'.format(
            self._check('id', id, int)), params=params).json()['response']

    def template_list(self, category=None, search=None, fields=None):
        '''
        Returns the list of audit file templates.

        :sc-api:`audit templates: list <AuditFile-Template.html#AuditFileTemplateRESTReference-/auditFileTemplate>`

        Args:
            category (int, optional):
                Restrict the results to only the specified category id.
            fields (list, optional):
                A list of attributes to return.
            search (str, optional):
                Restrict the response to only audit file names that match the
                search string specified.

        Returns:
            :obj:`list`:
                List of audit file records.

        Exmaples:
            >>> for tmpl in sc.audit_files.template_list():
            ...     pprint(tmpl)
        '''
        params = dict()

        if category:
            params['categoryID'] = self._check('category', category, int)

        if search:
            params['searchString'] = self._check('search', search, str)

        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('auditFileTemplate',
            params=params).json()['response']