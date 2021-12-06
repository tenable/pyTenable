'''
Tenable.ad session
'''
import warnings
import os

from tenable.base.platform import APIPlatform

from .about import AboutAPI
from .api_keys import APIKeyAPI
from .dashboard.api import DashboardAPI
from .directories.api import DirectoriesAPI
from .users.api import UsersAPI
from .widget.api import WidgetsAPI


class TenableAD(APIPlatform):
    _env_base = 'TAD'
    _base_path = 'api'
    _conv_json = True

    def _session_auth(self, **kwargs):
        msg = 'Session Auth isn\'t supported with the Tenable.ad APIs'
        warnings.warn(msg)
        self._log.warning(msg)

    def _key_auth(self, api_key):
        self._session.headers.update({
            'X-API-Key': f'{api_key}'
        })
        self._auth_mech = 'keys'

    def _authenticate(self, **kwargs):
        kwargs['_key_auth_dict'] = kwargs.get('_key_auth_dict', {
            'api_key': kwargs.get('api_key',
                                  os.getenv(f'{self._env_base}_API_KEY')
                                  )
        })
        super()._authenticate(**kwargs)

    @property
    def about(self):
        '''
        The interface object for the
        :doc:`Tenable.ad About APIs <about>`.
        '''
        return AboutAPI(self)

    @property
    def api_keys(self):
        '''
        The interface object for the
        :doc:`Tenable.ad API-Keys APIs <api_keys>`.
        '''
        return APIKeyAPI(self)

    @property
    def dashboard(self):
        '''
        The interface object for the
        :doc:`Tenable.ad Dashboard APIs <dashboard>`.
        '''
        return DashboardAPI(self)

    @property
    def directories(self):
        '''
        The interface object for the
        :doc:`Tenable.ad Directories APIs <directories>`.
        '''
        return DirectoriesAPI(self)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable.ad Users APIs <users>`.
        '''
        return UsersAPI(self)

    @property
    def widgets(self):
        '''
        The interface object for the
        :doc:`Tenable.ad Widget APIs <widget>`.
        '''
        return WidgetsAPI(self)
