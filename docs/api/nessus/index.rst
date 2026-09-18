Tenable Nessus
==============

.. important::
    The Nessus Package is currently a Technology Preview


Quick start
-----------

The following example connects to a Nessus server, displays its server type,
and lists the available scans:

.. code-block:: python

    from tenable.nessus import Nessus

    access_key = 'access-key-in-hex-goes-here'
    secret_key = 'secret-key-in-hex-goes-here'

    client = Nessus(
        url='https://nessus.example.com:8834/',
        access_key=access_key,
        secret_key=secret_key,
    )

    properties = client.server.properties()
    print(properties['nessus_type'])

    for scan in client.scans.list()['scans']:
        print(
            f"{scan['name']} - {scan['status']} - "
            f"{scan['scan_type']} - {scan['creation_date']}"
        )


.. automodule:: tenable.nessus.api
