'''
Tenable Identity Exposure session
'''
import warnings
import os

from tenable.base.platform import APIPlatform

from .about import AboutAPI
from .api_keys import APIKeyAPI
from .attack_types.api import AttackTypesAPI
from .category.api import CategoryAPI
from .checker.api import CheckerAPI
from .checker_option.api import CheckerOptionAPI
from .dashboard.api import DashboardAPI
from .directories.api import DirectoriesAPI
from .infrastructure.api import InfrastructureAPI
from .ldap_configuration.api import LDAPConfigurationAPI
from .lockout_policy.api import LockoutPolicyAPI
from .preference.api import PreferenceAPI
from .profiles.api import ProfilesAPI
from .reason.api import ReasonAPI
from .roles.api import RolesAPI
from .saml_configuration.api import SAMLConfigurationAPI
from .score.api import ScoreAPI
from .topology.api import TopologyAPI
from .users.api import UsersAPI
from .widget.api import WidgetsAPI


class TenableAD(APIPlatform):
    _env_base = 'TAD'
    _base_path = 'api'
    _conv_json = True

    def _session_auth(self, **kwargs):
        msg = 'Session Auth isn\'t supported with the Tenable Identity Exposure APIs'
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
        :doc:`Tenable Identity Exposure About APIs <about>`.
        '''
        return AboutAPI(self)

    @property
    def api_keys(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure API-Keys APIs <api_keys>`.
        '''
        return APIKeyAPI(self)

    @property
    def attack_types(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Attack Types APIs <attack_types>`.
        '''
        return AttackTypesAPI(self)

    @property
    def category(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Category APIs <category>`.
        '''
        return CategoryAPI(self)

    @property
    def checker(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Checker APIs <checker>`.
        '''
        return CheckerAPI(self)

    @property
    def checker_option(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Checker option APIs <checker_option>`.
        '''
        return CheckerOptionAPI(self)

    @property
    def dashboard(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Dashboard APIs <dashboard>`.
        '''
        return DashboardAPI(self)

    @property
    def directories(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Directories APIs <directories>`.
        '''
        return DirectoriesAPI(self)

    @property
    def infrastructure(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Infrastructure APIs <infrastructure>`.
        '''
        return InfrastructureAPI(self)

    @property
    def ldap_configuration(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure LDAP Configuration APIs <ldap_configuration>`.
        '''
        return LDAPConfigurationAPI(self)

    @property
    def lockout_policy(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Lockout Policy APIs <lockout_policy>`.
        '''
        return LockoutPolicyAPI(self)
      
    @property
    def preference(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Preference APIs <preference>`.
        '''
        return PreferenceAPI(self)

    @property
    def profiles(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Profiles APIs <profiles>`.
        '''
        return ProfilesAPI(self)

    @property
    def reason(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Reason APIs <reason>`.
        '''
        return ReasonAPI(self)

    @property
    def roles(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Roles APIs <roles>`.
        '''
        return RolesAPI(self)

    @property
    def saml_configuration(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure SAML configuration APIs <saml_configuration>`.
        '''
        return SAMLConfigurationAPI(self)

    @property
    def score(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Score APIs <score>`.
        '''
        return ScoreAPI(self)

    @property
    def topology(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Topology APIs <topology>`.
        '''
        return TopologyAPI(self)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Users APIs <users>`.
        '''
        return UsersAPI(self)

    @property
    def widgets(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Widget APIs <widget>`.
        '''
        return WidgetsAPI(self)
