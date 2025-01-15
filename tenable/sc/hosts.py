"""
HOSTS
=====

The following methods allow for interaction into the Tenable Security Center
:sc-api:`Hosts <Hosts.htm>` API.

Methods available on ``sc.hosts``:

.. rst-class:: hide-signature
.. autoclass:: HostsAPI
    :members:
"""

from .base import SCEndpoint


class HostsAPI(SCEndpoint):
    def list(self, fields=None):
        """
        Retrieves the list of hosts.
        :sc-api:`hosts: list <Hosts.htm#HostsRESTReference-/hosts>`

        Args:
            fields (list, optional):
                A list of attributes to return for each host.
        Returns:
            :obj:`dict`:
                The list of hosts.

        Examples:
            >>> for host in sc.hosts.list():
            ...     pprint(host)
        """
        params = dict()
        if fields:
            params["fields"] = ",".join([self._check("field", f, str) for f in fields])

        return self._api.get('hosts', params=params).json()['response']
