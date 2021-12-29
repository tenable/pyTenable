'''
Tenable.ad
==========

This package covers the Tenable.ad interface.

.. autoclass:: TenableAD
    :members:


.. toctree::
    :hidden:
    :glob:

    about
    api_keys
    attack_types
    category
    checker
    dashboard
    directories
    infrastructure
    ldap_configuration
    lockout_policy
    preference
    profiles
    roles
    saml_configuration
    score
    users
    widget
'''
from .session import TenableAD  # noqa: F401
