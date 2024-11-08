'''
Syslog
======

Methods described in this section relate to the syslog API.
These methods can be accessed at ``TenableIE.syslog``.

.. rst-class:: hide-signature
.. autoclass:: SyslogAPI
    :members:
'''
from typing import List, Dict
from marshmallow import ValidationError
from tenable.ie.syslog.schema import SyslogSchema
from tenable.base.endpoint import APIEndpoint


class SyslogAPI(APIEndpoint):
    _path = 'syslogs'
    _schema = SyslogSchema()
    _long_var = 'should_notify_on_initial_full_security_check'

    def list(self) -> List[Dict]:
        '''
        Returns all the syslog objects.

        Returns:
            list:
                The list of syslog objects.

        Examples:
            >>> tie.syslog.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self, **kwargs) -> List[Dict]:
        '''
        Creates a syslog object.

        Args:
            profiles (List[int]):
                The list of profile identifiers.
            checkers (List[int], required_for=[``deviances``]):
                The list of checker identifiers.
            input_type (str):
                The type of input to send through the syslog.
                Allowed values are ``deviances`` or
                ``ad_object_changes`` or ``attacks``.
            description (optional, str):
                The description for syslog object.
            attack_types (List[int], required_for=[``attacks``]):
                Filter on the types of attack that will be sent if
                input type is ``attack``.
            ip (str):
                The collector ip address or hostname of the syslog.
            port (int):
                The port number of the collector ip address.
            protocol (str):
                The protocol used by the collector. Allowed values
                are ``TCP`` and ``UDP``.
            tls (bool, required_for=[``TCP``]):
                Whether the configured syslog should connect using TLS.
                By default and if ``UDP`` is selected as the
                protocol, tls is ``False``.
            criticity_threshold (int, required_for=[``attacks``, \
            ``deviances``]):
                Threshold at which indicator alerts will be sent.
            directories (list[str]):
                The list of directory identifiers.
            should_notify_on_initial_full_security_check (bool):
                Whether alerts should be sent when deviances are
                detected during the initial analysis phase.
            filter_expression (optional, mapping):
                An object describing a filter for searched items.

        Returns:
            list[dict]:
                The created syslog object.

        Example:
            Create a syslog object with input_type as
            ``ad_object_changes``.

            >>> tie.syslog.create(
            ...     description='test_syslog',
            ...     input_type="ad_object_changes",
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=False,
            ...     directories=[2],
            ...     should_notify_on_initial_full_security_check=False,
            ...     filter_expression={'OR': [{'systemOnly': 'True'}]}
            ...     )

            Create syslog object with input_type as ``attacks``

            >>> tie.syslog.create(
            ...     description='test_syslog',
            ...     input_type="attacks",
            ...     profiles=[1],
            ...     attack_types=[1],
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=True,
            ...     criticity_threshold=55,
            ...     directories=[2],
            ...     should_notify_on_initial_full_security_check=False,
            ...     filter_expression={'OR': [{'systemOnly': 'True'}]}
            ...     )

            Create syslog object with input_type as ``deviances``

            >>> tie.syslog.create(
            ...     description='test_syslog',
            ...     input_type="deviances",
            ...     profiles=[1],
            ...     checkers=[1],
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=True,
            ...     criticity_threshold=55,
            ...     directories=[2],
            ...     should_notify_on_initial_full_security_check=False,
            ...     filter_expression={'OR': [{'systemOnly': 'True'}]}
            ...     )

            Create syslog object with protocol as ``UDP`` without
            passing ``tls``

            >>> tie.syslog.create(
            ...     description='test_syslog',
            ...     input_type="deviances",
            ...     profiles=[1],
            ...     checkers=[1],
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="UDP",
            ...     criticity_threshold=55,
            ...     directories=[2],
            ...     should_notify_on_initial_full_security_check=False,
            ...     filter_expression={'OR': [{'systemOnly': 'True'}]})
                '''
        if kwargs.get('input_type') == 'deviances':
            payload = [self._schema.dump(
                self._schema.load(kwargs, partial=('attack_types', )))]

        elif kwargs.get('input_type') == 'ad_object_changes':
            partial = ('attack_types', 'checkers', 'profiles',
                       'criticity_threshold', )
            payload = [self._schema.dump(
                self._schema.load(kwargs, partial=partial))]

        elif kwargs.get('input_type') == 'attacks':
            payload = [self._schema.dump(
                self._schema.load(kwargs, partial=('checkers', )))]

        else:
            message = 'input_type must be one of deviances, attacks, ' \
                      'ad_object_changes'
            raise ValidationError(message=message)
        return self._schema.load(self._post(json=payload), many=True)

    def details(self, syslog_id: str) -> Dict:
        '''
        Returns the details of the syslog object of the given syslog
        identifier.

        Args:
            syslog_id (str):
                The syslog object identifier.

        Returns:
            dict:
                The details of the syslog object.

        Examples:
            >>> tie.syslog.details(syslog_id='1')
        '''
        return self._schema.load(self._get(f'{syslog_id}'))

    def update(self, syslog_id: str, **kwargs) -> Dict:
        '''
        Updates the existing syslog object.

        Args:
            syslog_id (str):
                The syslog object identifier.
            profiles (optional, List[int]):
                The list of profile identifiers.
            checkers (optional, List[int], required_for=[``deviances``]):
                The list of checker identifiers.
            input_type (optional, str):
                The type of input to send through the syslog.
                Allowed values for ``deviances`` or
                ``ad_object_changes`` or ``attacks``.
            description (optional, str):
                The description for syslog object.
            attack_types (optional, List[int], required_for=[``attacks``]):
                Filter on the types of attack that will be sent if
                input type is ``attack``.
            ip (optional, str):
                The collector ip address or hostname of the syslog.
            port (optional, int):
                The port number of the collector ip address.
            protocol (optional, str):
                The protocol used by the collector. Allowed values
                are ``TCP`` and ``UDP``.
            tls (optional,  bool, required if protocol is ``tcp``):
                Whether the configured syslog should connect using TLS.
                By default and if ``UDP`` is selected as the
                protocol, tls is ``False``.
            criticity_threshold (optional, int, required_for=[``attacks``, \
            ``deviances``]):
                Threshold at which indicator alerts will be sent.
            directories (optional, list[str]):
                The list of directory identifiers.
            should_notify_on_initial_full_security_check (bool):
                Whether alerts should be sent when deviances are
                detected during the initial analysis phase.
            filter_expression (optional, mapping):
                An object describing a filter for searched items.

        Returns:
            dict:
                The updated syslog object.

        Examples:
            >>> tie.syslog.update(
            ...     syslog_id='1',
            ...     filter_expression={'OR': [{'systemOnly': 'True'}]}
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs, partial=True))
        return self._schema.load(self._patch(f'{syslog_id}', json=payload))

    def delete(self, syslog_id: str) -> None:
        '''
        Deletes the syslog object of given syslog identifier.

        Args:
            syslog_id (str):
                The syslog object identifier.

        Returns:
            None:

        Examples:
            >>> tie.syslog.delete(syslog_id='1')
        '''
        self._delete(f'{syslog_id}')

    def send_syslog_notification_by_id(self, syslog_id: str) -> None:
        '''
        Send a test syslog notification by syslog identifier.

        Args:
            syslog_id (str):
                The syslog object identifier.

        Returns:
            None:

        Examples:
            >>> tie.syslog.send_syslog_notification_by_id(syslog_id='1')
        '''
        self._schema.load(self._get(f'test-message/{syslog_id}'),
                          many=True)

    def send_notification(self, **kwargs) -> None:
        '''
        Send a test syslog notification.

        Args:
            profiles (List[int]):
                The list of profile identifiers.
            checkers (optional, List[int], required_for=[``deviances``]):
                The list of checker identifiers.
            input_type (str):
                The type of input to send through the syslog.
                Allowed values for ``deviances`` or
                ``ad_object_changes`` or ``attacks``.
            description (optional, str):
                The description for syslog object.
            attack_types (optional, List[int], required_for=[``attacks``]):
                Filter on the types of attack that will be sent if
                input type is ``attack``.
            ip (str):
                The collector ip address or hostname of the syslog.
            port (int):
                The port number of the collector ip address.
            protocol (str):
                The protocol used by the collector. Allowed values
                are ``TCP`` and ``UDP``.
            tls (bool, required if protocol is ``tcp``):
                Whether the configured syslog should connect using TLS.
                By default and if ``UDP`` is selected as the
                protocol, tls is ``False``.
            criticity_threshold (int, required_for=[``attacks``, \
            ``deviances``]):
                Threshold at which indicator alerts will be sent.
            directories (list[str]):
                The list of directory identifiers.

        Returns:
            None:

        Examples:
            Send test syslog with input_type as ``ad_object_changes``.

            >>> tie.syslog.send_notification(
            ...     input_type="ad_object_changes",
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=True,
            ...     directories=[2],
            ...     )

            Send test syslog with input_type as ``deviances``.

            >>> tie.syslog.send_notification(
            ...     checkers=[1],
            ...     profiles=[1],
            ...     input_type="deviances",
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=True,
            ...     criticity_threshold=10,
            ...     directories=[2],
            ...     )

            Send test syslog with input_type as ``attacks``

            >>> tie.syslog.send_notification(
            ...     profiles=[1],
            ...     input_type="attacks",
            ...     attack_types=[1],
            ...     ip='127.0.0.1',
            ...     port=8888,
            ...     protocol="TCP",
            ...     tls=True,
            ...     criticity_threshold=10,
            ...     directories=[2],
            ...     )
        '''
        if kwargs.get('input_type') == 'deviances':
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=('attack_types',
                                                   self._long_var, )))
        elif kwargs.get('input_type') == 'ad_object_changes':
            partial = ('attack_types', 'checkers', 'profiles',
                       'criticity_threshold', self._long_var, )
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=partial))

        elif kwargs.get('input_type') == 'attacks':
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=('checkers',
                                                   self._long_var, )))
        else:
            message = 'input_type must be one of deviances, attacks, ' \
                      'ad_object_changes'
            raise ValidationError(message=message)
        self._schema.load(self._post('test-message', json=payload),
                          many=True)
