SecurityCenter
==========
.. py:module:: tenable.sc


Connecting to SecurityCenter
------------------------

Some stuff here....

Client reference
----------------

.. autoclass:: SecurityCenter

    .. autoattribute:: login
    .. autoattribute:: logout
    .. autoattribute:: agents
    .. autoattribute:: alerts
    .. autoattribute:: analysis
    .. autoattribute:: arcs
    .. autoattribute:: asset_lists
    .. autoattribute:: blackouts
    .. autoattribute:: dashboards
    .. autoattribute:: jobs
    .. autoattribute:: notifications
    .. autoattribute:: reports
    .. autoattribute:: repository
    .. autoattribute:: risk
    .. autoattribute:: scans
    .. autoattribute:: sensors
    .. autoattribute:: system
    .. autoattribute:: tickets
    .. autoattribute:: users

.. toctree::
   :maxdepth: 2
   :hidden:

   sc.agents
   sc.alerts
   sc.analysis
   sc.arcs
   sc.asset_lists
   sc.blackouts
   sc.dashboards
   sc.jobs
   sc.notifications
   sc.reports
   sc.repository
   sc.risk
   sc.scans
   sc.sensors
   sc.system
   sc.tickets
   sc.users
   

Lower-Level Calls
-----------------

.. rst-class:: hide-signature
.. py:class:: SecurityCenter

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete