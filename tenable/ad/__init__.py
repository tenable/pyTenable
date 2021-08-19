'''
.. autoclass:: TenableAD

.. automodule:: tenable.ad.about
.. automodule:: tenable.ad.ad_object
.. automodule:: tenable.ad.alert
.. automodule:: tenable.ad.api_key
.. automodule:: tenable.ad.application_setting
.. automodule:: tenable.ad.attack_alert
.. automodule:: tenable.ad.attack
.. automodule:: tenable.ad.category
.. automodule:: tenable.ad.checker
.. automodule:: tenable.ad.checker_option
.. automodule:: tenable.ad.dashboard
.. automodule:: tenable.ad.deviance
.. automodule:: tenable.ad.directory
.. automodule:: tenable.ad.email_notifier
.. automodule:: tenable.ad.event
.. automodule:: tenable.ad.infrastructure
.. automodule:: tenable.ad.ldap_configuration
.. automodule:: tenable.ad.license
.. automodule:: tenable.ad.preference
.. automodule:: tenable.ad.profile
.. automodule:: tenable.ad.reason
.. automodule:: tenable.ad.role
.. automodule:: tenable.ad.saml_configuration
.. automodule:: tenable.ad.score
.. automodule:: tenable.ad.syslog
.. automodule:: tenable.ad.topology
.. automodule:: tenable.ad.user
.. automodule:: tenable.ad.widget

Raw HTTP Calls
==============

Even though the ``TenableAD`` object pythonizes the Tenable.AD API for you,
there may still bee the occasional need to make raw HTTP calls to the AD API.
The methods listed below aren't run through any naturalization by the library
aside from the response code checking.  These methods effectively route
directly into the requests session.  The responses will be Response objects from
the ``requests`` library.  In all cases, the path is appended to the base
``url`` parameter that the ``TenableAD`` object was instantiated with.

Example:

.. code-block:: python

    import requests

    url = "https://customer.tenable.ad/api/about"

    headers = {"Accept": "application/json", "x-api-key":"ffffffff-ffff-ffff-ffff-ffffffffffff"}

    response = requests.request("GET", url, headers=headers)

    print(response.text)

.. py:module:: tenable.ad
.. rst-class:: hide-signature
.. py:class:: TenableAD

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from __future__ import absolute_import

from tenable.ad.about import AboutApi
# import apis into api package
from tenable.ad.ad_object import ADObjectApi
from tenable.ad.alert import AlertApi
from tenable.ad.api_key import APIKeyApi
from tenable.ad.application_setting import ApplicationSettingApi
from tenable.ad.attack_alert import AttackAlertApi
from tenable.ad.attack import AttackApi
from tenable.ad.category import CategoryApi
from tenable.ad.checker import CheckerApi
from tenable.ad.checker_option import CheckerOptionApi
from tenable.ad.dashboard import DashboardApi
from tenable.ad.deviance import DevianceApi
from tenable.ad.directory import DirectoryApi
from tenable.ad.email_notifier import EmailNotifierApi
from tenable.ad.event import EventApi
from tenable.ad.infrastructure import InfrastructureApi
from tenable.ad.ldap_configuration import LDAPConfigurationApi
from tenable.ad.license import LicenseApi
from tenable.ad.preference import PreferenceApi
from tenable.ad.profile import ProfileApi
from tenable.ad.reason import ReasonApi
from tenable.ad.role import RoleApi
from tenable.ad.saml_configuration import SAMLConfigurationApi
from tenable.ad.score import ScoreApi
from tenable.ad.syslog import SyslogApi
from tenable.ad.topology import TopologyApi
from tenable.ad.user import UserApi
from tenable.ad.widget import WidgetApi
from tenable.base import APISession


class TenableAD(APISession):
    @property
    def about(self):
        return AboutApi(self)

    @property
    def ad_object(self):
        return ADObjectApi(self)

    @property
    def alert(self):
        return AlertApi(self)

    @property
    def api_key(self):
        return APIKeyApi(self)

    @property
    def application_setting(self):
        return ApplicationSettingApi(self)

    @property
    def attack_alert(self):
        return AttackAlertApi(self)

    @property
    def attack(self):
        return AttackApi(self)

    @property
    def category(self):
        return CategoryApi(self)

    @property
    def checker(self):
        return CheckerApi(self)

    @property
    def checker_option(self):
        return CheckerOptionApi(self)

    @property
    def dashboard(self):
        return DashboardApi(self)

    @property
    def deviance(self):
        return DevianceApi(self)

    @property
    def directory(self):
        return DirectoryApi(self)

    @property
    def email_notifier(self):
        return EmailNotifierApi(self)

    @property
    def event(self):
        return EventApi(self)

    @property
    def infrastructure(self):
        return InfrastructureApi(self)

    @property
    def ldap_configuration(self):
        return LDAPConfigurationApi(self)

    @property
    def license(self):
        return LicenseApi(self)

    @property
    def preference(self):
        return PreferenceApi(self)

    @property
    def profile(self):
        return ProfileApi(self)

    @property
    def reason(self):
        return ReasonApi(self)

    @property
    def role(self):
        return RoleApi(self)

    @property
    def saml_configuration(self):
        return SAMLConfigurationApi(self)

    @property
    def score(self):
        return ScoreApi(self)

    @property
    def syslog(self):
        return SyslogApi(self)

    @property
    def topology(self):
        return TopologyApi(self)

    @property
    def user(self):
        return UserApi(self)

    @property
    def widget(self):
        return WidgetApi(self)

    @property
    def widget(self):
        return WidgetApi(self)
