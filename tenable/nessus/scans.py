'''
Scans
=====

Methods described in this section relate to the scans API.
These methods can be accessed at ``Nessus.scans``.

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:
'''
from typing import Dict, List, Optional
from io import BytesIO
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint
from .schema.scans import ScanExportSchema


class ScansAPI(APIEndpoint):
    _path = 'scans'

    def attachment(self,
                   scan_id: int,
                   attachment_id: int,
                   key: str,
                   fobj: Optional[BytesIO] = None
                   ) -> BytesIO:
        '''
        Returns the requested attachment file

        Args:
            scan_id (int): The Scan to fetch from
            attachment_id (int): The id of the scan attachment
            key (str): The access token for the attachment
            fobj (BytesIO, optional): File object to write to

        Returns:
            BytesIO:
                The file object requested

        Example:

            >>> with open('example.png', 'wb') as image_file:
            ...     nessus.scans.attachment(1, 1, 'something', image_file)
        '''
        if not fobj:
            fobj = BytesIO()

        resp = self._get(f'{scan_id}/attachments/{attachment_id}',
                         params={'key': key},
                         stream=True
                         )
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def configure(self, scan_id: int, **kwargs) -> None:
        '''
        Reconfigures an existing scan.

        Args:
            scan_id (int): Id of the scan to modify
            **kwargs: the various settings to pass

        Return:
            Dict:
                The updated scan object

        Example:

            >>> nessus.scans.configure(1, settings={
            ...     'name': 'Example Scan',
            ...     'enabled': True,
            ...     'text_targets': '192.168.1.1'
            ... })
        '''
        return self._put(f'{scan_id}', json=kwargs)

    def copy(self,
             scan_id: int,
             folder_id: Optional[int] = None,
             name: Optional[str] = None
             ) -> Dict:
        '''
        Copies the scan object

        Args:
            scan_id (int): Id of the scan to copy
            folder_id (int, optional): Id of the destination folder
            name (str, optional): Name of the copied scan

        Returns:
            Dict:
                The copied scan object

        Example:

            >>> nessus.scans.copy(1)
        '''
        return self._post(f'{scan_id}/copy', json=dict_clean({
            'folder_id': folder_id,
            'name': name
        }))

    def create(self, **kwargs) -> Dict:
        '''
        Creates a new scan

        Args:
            **kwargs:
                The parameters to pass to the API to create the scan.  For
                information on what to pass here, consult the API documentation

        Returns:
            Dict:
                The created scan object

        Example:

            >>> nessus.scans.create(uuid='abcdef12345667890abcdef',
                                    settings={
                                        'name': 'Example Scan',
                                        'enabled': False,
                                        'text_targets': '192.168.1.1'
                                    })
        '''
        return self._post(json=kwargs)

    def delete(self, scan_id: int) -> None:
        '''
        Deletes the specified scan object

        Args:
            scan_id (int): Id of the scan to delete

        Example:

            >>> nessus.scans.delete(1)
        '''
        self._delete(f'{scan_id}')

    def delete_many(self, scan_ids: List[int]) -> List:
        '''
        Deletes multiple scan objects

        Args:
            scan_ids (List[int]): List of scan ids to delete

        Returns:
            List:
                list of deleted scans

        Example:

            >>> nessus.scans.delete_many([1, 2, 3])
        '''
        return self._delete(json={'ids': scan_ids})['deleted']

    def delete_history(self, scan_id: int, history_id: int) -> None:
        '''
        Deletes the specified history object within a scan.

        Args:
            scan_id (int): The scan to modify
            history_id (int): Id of the history object to remove

        Example:

            >>> nessus.scans.delete_history(1, 1)
        '''
        self._delete(f'{scan_id}/history/{history_id}')

    def details(self, scan_id: int) -> Dict:
        '''
        Returns the details for the specified scan.

        Args:
            scan_id (int): Id of the scan to retrieve

        Example:

            >>> nessus.scans.details(1)
        '''
        return self._get(f'{scan_id}')

    def export_formats(self,
                       scan_id: int,
                       schedule_id: Optional[int] = None
                       ) -> Dict:
        '''
        Returns the available export formats and report options.

        Args:
            scan_id (int): The scan to export
            schedule_id (int, optional):
                The schedule id associated with the scan

        Returns:
            Dict:
                The available export and report options

        Example:

            >>> nessus.scans.export_formats(1)
        '''
        return self._get(f'{scan_id}/export/formats', params=dict_clean({
            'schedule_id': schedule_id
        }))

    def export_scan(self,
                    scan_id: int,
                    history_id: Optional[int] = None,
                    fobj: Optional[BytesIO] = None,
                    **kwargs
                    ) -> BytesIO:
        '''
        Generate a scan export or report and download it.

        Args:
            scan_id (int): The id of the scan to export.
            history_id (int, optional):
                The history id of the specific point in time to export.
            fobj (BytexIO, optional):
                The file object to write the exported file to.  If none is
                specified then a BytesIO object is written to in memory.
            filters (list[tuple], optional):
                The filters to apply to the exported data.
            format (str, optional):
                The exported scan format.  Supported values are ``nessus``,
                ``html``, ``csv``, and ``db``.  If unspecified, the default is
                ``nessus``.
            password (str, optional):
                The password to apply to the exported data (required for db).
            template_id (int, optional):
                When exporting in HTML or PDF, what report definition should
                the exported data be represented within.
            chunk_size (int, optional):
                The chunk sizing for the download itself.
            stream_hook (callable, optional):
                Overload the default downloading behavior with a custom
                stream hook.
            hook_kwargs (dict, optional):
                keyword arguments to pass to the stream_hook callable in
                addition to the default passed params.
        '''
        dlopts = {
            'fobj': fobj,
            'chunk_size': kwargs.pop('chunk_size', None),
            'stream_hook': kwargs.pop('stream_hook', None),
            'hook_kwargs': kwargs.pop('hook_kwargs', None)
        }
        schema = ScanExportSchema()
        payload = dict_clean(schema.dump(schema.load(kwargs)))
        token = self._post(f'{scan_id}/export',
                           params=dict_clean({'history_id': history_id}),
                           json=payload
                           )['token']
        return self._api.tokens._fetch(token, **dlopts)  # noqa PLW0212

    def import_scan(self,
                    fobj: Optional[BytesIO] = None,
                    file_id: Optional[str] = None,
                    folder_id: Optional[int] = None,
                    password: Optional[str] = None
                    ) -> Dict:
        '''
        Import a scan report into the Tenable Nessus scanner.  Either a file object or
        a file_id must be specified.

        Args:
            fobj (BytesIO, optional):
                The file object to import.
            file_id (str, optional):
                The id of the already uploaded file object to import.
            folder_id (int, optional):
                The folder that the imported scan should reside within.
            password (str, optional):
                If the file object is encrypted, this password will be used
                to decrypt.

        Example:

            >>> with open('Example.nessus', 'rb') as reportfile:
            ...     nessus.scans.import_scan(reportfile)
        '''
        if not file_id:
            file_id = self._api.files.upload(fobj)
        return self._post('import', json=dict_clean({
            'file': file_id,
            'folder_id': folder_id,
            'password': password
        }))

    def kill(self, scan_id: int) -> None:
        '''
        Forcefully terminate the currently running scan.

        Args:
            scan_id (int): The id of the scan to terminate.

        Example:

            >>> nessus.scans.kill(1)
        '''
        self._post(f'{scan_id}/kill')

    def launch(self,
               scan_id: int,
               alt_targets: Optional[List[str]] = None
               ) -> str:
        '''
        Launch a configured scan.

        Args:
            scan_id (int):
                The id of the scan to launch.
            alt_targets (list[str], optional):
                A List of alternative targets to run the scan against.

        Example:

            >>> nessus.scan.launch(1)
        '''
        return self._post(f'{scan_id}/launch',
                          json=dict_clean({'alt_targets': alt_targets})
                          )['scan_uuid']

    def list(self,
             folder_id: Optional[int] = None,
             last_modification_date: Optional[int] = None
             ) -> Dict:
        '''
        List of the available scan objects.

        Args:
            folder_id (int, optional):
                Restrict the results to only the specified folder id.
            last_modification_date (int, optional):
                Restrict the results to only scans modified after the
                specified timestamp.

        Example:

            >>> for scan in nessus.scans.list():
            ...     print(scan)
        '''
        return self._get(params=dict_clean({
            'folder_id': folder_id,
            'last_modification_date': last_modification_date
        }))

    def pause(self, scan_id: int) -> None:
        '''
        Pauses a currently running scans.

        Args:
            scan_id (int): The id of the scan to pause.

        Example:

            >>> nessus.scans.pause(1)
        '''
        self._post(f'{scan_id}/pause')

    def plugin_output(self,
                      scan_id: int,
                      host_id: int,
                      plugin_id: int,
                      history_id: Optional[int] = None
                      ) -> Dict:
        '''
        Returns the plugin output for a specific finding within a scan.

        Args:
            scan_id (int): The id of the scan
            host_id (int): The id of the host within the scan
            plugin_id (int): The plugin id of the finding on the host
            history_id (int, optional):
                The id of the history object within the scan.

        Returns:
            Dict:
                The restuls of the specific finding specified.

        Example:

            >>> nessus.scans.plugin_output(1, 1, 19506)
        '''
        return self._get(f'{scan_id}/hosts/{host_id}/plugins/{plugin_id}',
                         params=dict_clean({'history_id': history_id})
                         )

    def read_status(self, scan_id: int, read: bool) -> None:
        '''
        Sets the read status for the given scan.

        Args:
            scan_id (int): The id of the scan to modify
            read (bool): Is the scan read?

        Example:

            >>> nessus.scans.read_status(1, True)
        '''
        self._put(f'{scan_id}/status', params={'read': str(read).lower()})

    def resume(self, scan_id: int) -> None:
        '''
        Resumes a paused scan.

        Args:
            scan_id (int): The id of the scan to resume.

        Example:

            >>> nessus.scans.resume(1)
        '''
        self._post(f'{scan_id}/resume')

    def schedule(self, scan_id: int, enabled: bool) -> Dict:
        '''
        Enables/Disables the scan schedule for the given scan.

        Args:
            scan_id (int):
                The id of the scan to modify
            enabled (bool):
                Should the scan schedule be enabled?

        Returns:
            Dict:
                The scan schedule settings.
        '''
        return self._put(f'{scan_id}/schedule',
                         params={'enabled': str(enabled).lower()}
                         )

    def stop(self, scan_id: int) -> None:
        '''
        Stops a running scan

        Args:
            scan_id (int): The id of the scan to stop.

        Example:

            >>> nessus.scans.stop(1)
        '''
        return self._post(f'{scan_id}/stop')

    def timezones(self) -> List[Dict]:
        '''
        Returns the currently configured timezone data

        Returns:
            List[Dict]:
                List of timezone objects

        Example:

            >>> nessus.scans.timezones()
        '''
        return self._get('timezones')['timezones']
