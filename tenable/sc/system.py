'''
system
======

The following methods allow for interaction into the Tenable.sc
:sc-api:`System <System.html>` API.  These API calls are typically used to
understand timezones, system version, etc.

Methods available on ``sc.system``:

.. rst-class:: hide-signature
.. autoclass:: SystemAPI

    .. automethod:: current_locale
    .. automethod:: details
    .. automethod:: diagnostics
    .. automethod:: list_locales
    .. automethod:: set_locale
    .. automethod:: status
'''
from .base import SCEndpoint
from io import BytesIO
import time

class SystemAPI(SCEndpoint):
    def details(self):
        '''
        Retrieves information about the Tenable.sc instance.  This method should
        only be called before authentication has occurred.  As most of the
        information within this call already happens upon instantiation, there
        should be little need to call this manually.

        :sc-api:'system: get <System.html#system_GET>`

        Returns:
            :obj:`dict`:
                The response dictionary

        Examples:
            >>> info = sc.system.details()
        '''
        return self._api.get('system').json()['response']

    def diagnostics(self, task=None, options=None, fobj=None):
        '''
        Generates and downloads a diagnostic file for the purpose of
        troubleshooting an ailing Tenable.sc instance.

        :sc-api:`system: diagnostics-generate <System.html#SystemRESTReference-/system/diagnostics/generate>`

        :sc-api:`system: diagnostics-download <System.html#SystemRESTReference-/system/diagnostics/download>`

        Args:
            fobj (FileObject, optional):
                The file-like object to write the diagnostics file to.  If
                nothing is specified, a BytesIO object will be returnbed with
                the file.
            options (list, optional):
                If performing a diagnostics generation, then which items
                should be bundled into the diagnostics file?  Available options
                are ``all``, ``apacheLog``, ``configuration``, ``dependencies``,
                ``dirlist``, ``environment``, ``installLog``, ``logs``,
                ``sanitize``, ``scans``, ``serverConf``, ``setup``, ``sysinfo``,
                and ``upgradeLog``.  If nothing is specified, it will default to
                ``['all']``.
            task (str, optional):
                Which task to perform.  Available options are ``appStatus`` and
                ``diagnosticsFile``.  If nothing is specified, it will default
                to ``diagnosticFile``.

        Returns:
            :obj:`FileObject`:
                A file-like object with the diagnostics file specified.

        Examples:
            >>> with open('diagnostics.tar.gz', 'wb') as fobj:
            ...     sc.system.diagnostics(fobj=fobj)
        '''
        payload = {
            'task': self._check('task', task, str,
                choices=['diagnosticsFile', 'appStatus'],
                default='diagnosticsFile'),
        }

        # The available choices for the options.
        opts = ['all', 'apacheLog', 'configuration', 'dependencies',
            'dirlist', 'environment', 'installLog', 'logs', 'sanitize', 'scans',
            'serverConf', 'setup', 'sysinfo']

        # we only want to add the options to the generation call if the task is
        # a diagnostics file.
        if payload['task'] == 'diagnosticsFile':
            payload['options'] = [self._check('option:item', o, str, choices=opts)
                for o in self._check('options', options, list, default=['all'])]
        status = self.status()

        # Make the call to generate the disagnostics file.
        self._api.post('system/diagnostics/generate', json=payload)

        # We will sleep until the file has been generated.  We will know when
        # the file is ready or download as the `diagnosticsGenerated` timestamp
        # will have been updated.
        while self.status()['diagnosticsGenerated'] == status['diagnosticsGenerated']:
            time.sleep(5)

        # Make the call to download the file.
        resp = self._api.post('system/diagnostics/download', stream=True)

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

    def current_locale(self):
        '''
        Retreives the current system locale that Tenable.sc has been set to.

        :sc-api:`system: locale <System.html#SystemRESTReference-/system/locale>`

        Returns:
            :obj:`dict`:
                locale resource

        Examples:
            >>> sc.system.current_locale()
        '''
        return self._api.get('system/locale').json()['response']

    def list_locales(self):
        '''
        Retreives the available system locales that Tenable.sc can be set to.

        :sc-api:`system: locales <System.html#SystemRESTReference-/system/locales>`

        Returns:
            :obj:`dict`:
                locales dictionary

        Examples:
            >>> sc.system.list_locales()
        '''
        return self._api.get('system/locales').json()['response']

    def set_locale(self, locale):
        '''
        Sets the system locale to be used.  This requires an administrator to
        perform this task and will be a global change.  The locale determines
        which pluginset language to use.

        :sc-api:`system: set-locale <System.html#system_locale_PATCH>`

        Args:
            locale (str): The plugin locale name

        Returns:
            :obj:`str`:
                The new plugin locale.

        Examples:
            Set the system locale to Japanese:

            >>> sc.system.set_locale('ja')
        '''
        self._api.patch('system/locale', json={
                'PluginLocale': self._check('locale', locale, str)
            }).json()['response']

    def status(self):
        '''
        Retrieves the current system status

        :sc-api:`system: diagnostics <System.html#SystemRESTReference-/system/diagnostics>`

        Returns:
            :obj:`dict`:
                The status dictionary

        Examples:
            >>> status = sc.system.status()
        '''
        return self._api.get('system/diagnostics').json()['response']