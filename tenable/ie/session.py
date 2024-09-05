'''
Tenable Identity Exposure session
'''
import warnings
import os

from tenable.base.platform import APIPlatform

from .about import AboutAPI
from .ad_object.api import ADObjectAPI
from .alert.api import AlertsAPI
from .api_keys import APIKeyAPI
from .attack_type_options.api import AttackTypeOptionsAPI
from .application_settings.api import ApplicationSettingsAPI
from .attack_types.api import AttackTypesAPI
from .attacks.api import AttacksAPI
from .category.api import CategoryAPI
from .checker.api import CheckerAPI
from .checker_option.api import CheckerOptionAPI
from .dashboard.api import DashboardAPI
from .deviance.api import DevianceAPI
from .directories.api import DirectoriesAPI
from .email_notifiers.api import EmailNotifiersAPI
from .event.api import EventAPI
from .infrastructure.api import InfrastructureAPI
from .ldap_configuration.api import LDAPConfigurationAPI
from .license.api import LicenseAPI
from .lockout_policy.api import LockoutPolicyAPI
from .preference.api import PreferenceAPI
from .profiles.api import ProfilesAPI
from .reason.api import ReasonAPI
from .roles.api import RolesAPI
from .saml_configuration.api import SAMLConfigurationAPI
from .score.api import ScoreAPI
from .syslog.api import SyslogAPI
from .topology.api import TopologyAPI
from .users.api import UsersAPI
from .widget.api import WidgetsAPI


class TenableIE(APIPlatform):
    _env_base = 'TIE'
    _base_path = 'api'
    _conv_json = True
    _allowed_auth_mech_priority = ['key']
    _allowed_auth_mech_params = {
        'key': ['api_key']
    }

    def _key_auth(self, api_key):
        self._session.headers.update({
            'X-API-Key': f'{api_key}'
        })
        self._auth_mech = 'keys'

    @property
    def about(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure About APIs <about>`.
        '''
        return AboutAPI(self)

    @property
    def ad_object(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure AD Object APIs <ad_object>`.
        '''
        return ADObjectAPI(self)

    @property
    def alerts(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Alerts APIs <alert>`.
        '''
        return AlertsAPI(self)

    @property
    def api_keys(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure API-Keys APIs <api_keys>`.
        '''
        return APIKeyAPI(self)

    @property
    def attacks(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Attacks APIs <attacks>`.
        '''
        return AttacksAPI(self)

    @property
    def application_settings(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Application Settings APIs <application_settings>`.
        '''
        return ApplicationSettingsAPI(self)

    @property
    def attack_types(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Attack Types APIs <attack_types>`.
        '''
        return AttackTypesAPI(self)

    @property
    def attack_type_options(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Attack Type Options APIs <attack_type_options>`.
        '''
        return AttackTypeOptionsAPI(self)

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
    def deviance(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Deviance APIs <deviance>`.
        '''
        return DevianceAPI(self)

    @property
    def directories(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Directories APIs <directories>`.
        '''
        return DirectoriesAPI(self)

    @property
    def email_notifiers(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Email Notifiers APIs <email_notifiers>`.
        '''
        return EmailNotifiersAPI(self)

    @property
    def event(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Event APIs <event>`.
        '''
        return EventAPI(self)

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
    def license(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure License APIs <license>`.
        '''
        return LicenseAPI(self)

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
    def syslog(self):
        '''
        The interface object for the
        :doc:`Tenable Identity Exposure Syslog APIs <syslog>`.
        '''
        return SyslogAPI(self)

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
