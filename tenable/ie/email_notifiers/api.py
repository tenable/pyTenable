'''
Email Notifiers
===============

Methods described in this section relate to the email-notifier API.
These methods can be accessed at ``TenableIE.email_notifiers``.

.. rst-class:: hide-signature
.. autoclass:: EmailNotifiersAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.email_notifiers.schema import EmailNotifierSchema
from tenable.base.endpoint import APIEndpoint


class EmailNotifiersAPI(APIEndpoint):
    _path = 'email-notifiers'
    _schema = EmailNotifierSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all email notifiers instances

        Returns:
            list:
                The list of email notifier objects

        Examples:
            >>> tie.email_notifiers.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self,
               **kwargs
               ) -> List[Dict]:
        '''
        Create email notifiers

        Args:
            input_type (optional, str):
                The type of input. possible values are
                ``deviances`` and ``attacks``
            checkers (List[int], required_for=[``deviances``]):
                The list of checker identifiers.
            attack_types (List[int], required_for=[``attacks``]):
                The list of attack type identifiers.
            profiles (List[int]):
                The list of profile identifiers.
            address (str):
                The email address.
            should_notify_on_initial_full_security_check (bool):
                Whether alerts should be send when deviances are detected
                during the initial analysis phase?
            directories (list[str]):
                The list of directory identifiers.
            criticity_threshold (int):
                Threshold at which indicator alerts will be sent.
            description (optional, str):
                The description for notifier.

        Return:
            list[dict]:
                The created email notifiers instance objects

        Example:
            Create email notifier with input_type as deviances

            >>> tie.email_notifiers.create(
            ...     input_type='deviances',
            ...     checkers=[1, 2],
            ...     profiles=[1],
            ...     address='test@domain.com',
            ...     should_notify_on_initial_full_security_check=False,
            ...     directories=[1],
            ...     criticity_threshold=100,
            ...     description='test alert'
            ...     )

            Create email notifier with input_type as attacks

            >>> tie.email_notifiers.create(
            ...     input_type='attacks',
            ...     attack_types=[1, 2],
            ...     profiles=[1],
            ...     address='test@domain.com',
            ...     should_notify_on_initial_full_security_check=False,
            ...     directories=[1],
            ...     criticity_threshold=100,
            ...     description='test alert'
            ...     )
        '''
        if kwargs.get('input_type') == 'deviances':
            partial = ('attack_types',)
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=partial))
        else:
            partial = ('checkers',)
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=partial))

        return self._schema.load(self._post(json=[payload]), many=True)

    def details(self,
                email_notifier_id: str
                ) -> Dict:
        '''
        Retrieves the details for a specific email-notifier

        Args:
            email_notifier_id (str):
                The email-notifier instance identifier.

        Returns:
            dict:
                the email-notifier object.

        Examples:
            >>> tie.email_notifiers.details(
            ...     email_notifier_id='1'
            ...     )
        '''
        return self._schema.load(self._get(f'{email_notifier_id}'))

    def update(self,
               email_notifier_id: str,
               **kwargs
               ) -> Dict:
        '''
        Update an existing profile

        Args:
            email_notifier_id (str):
                The email-notifier instance identifier.
            address (optional, str):
                The email address.
            criticity_threshold (optional, int):
                Threshold at which indicator alerts will be sent.
            directories (optional, List[int]):
                The list of directory identifiers.
            description (optional, str):
                The description for notifier.
            checkers (optional, List[int]):
                The list of checker identfiers.
            attack_types (optional, List[int]):
                The list of attack type identifiers.
            profiles (optional, List[int]):
                The list of profile identifiers.
            input_type (optional, str):
                The type of input. possible values are
                ``deviances``, ``attacks``
            should_notify_on_initial_full_security_check (bool):
                Whether alerts should be send when deviances are detected
                during the initial analysis phase?

        Returns:
            dict:
                The updated email-notifier instance object.

        Examples:
            >>> tie.email_notifiers.update(
            ...     email_notifier_id='1',
            ...     input_type='attacks',
            ...     attack_types=[1, 2]
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs, partial=True))
        return self._schema.load(
            self._patch(f"{email_notifier_id}", json=payload))

    def delete(self, email_notifier_id: str) -> None:
        '''
        Delete an Email-Notifier instance

        Args:
            email_notifier_id (str):
                The profile instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.email_notifiers.delete(
            ...     email_notifier_id='1'
            ...     )
        '''
        self._delete(f"{email_notifier_id}")

    def send_test_email_by_id(self,
                              email_notifier_id: str
                              ) -> None:
        '''
        Send a test Email notification by id

        Args:
            email_notifier_id (str):
                The profile instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.email_notifiers.send_test_email_by_id(
            ...     email_notifier_id='1'
            ...     )
        '''
        self._get(f"test-message/{email_notifier_id}")

    def send_test_email(self,
                        **kwargs
                        ) -> None:
        '''
        Send a test Email notification

        Args:
            input_type (optional, str):
                The type of input. possible values are
                ``deviances`` and ``attacks``
            checkers (List[int], required_for=[``deviances``]):
                The list of checker identifiers.
            attack_types (List[int], required_for=[``attacks``]):
                The list of attack type identifiers.
            profiles (List[int]):
                The list of profile identifiers.
            address (str):
                The email address.
            directories (list[str]):
                The list of directory identifiers.
            criticity_threshold (int):
                Threshold at which indicator alerts will be sent.
            description (optional, str):
                The description for notifier.

        Returns:
            None:

        Examples:
            Send test email notifier with input_type as deviances

            >>> tie.email_notifiers.create(
            ...     input_type='deviances',
            ...     checkers=[1, 2],
            ...     profiles=[1],
            ...     address='test@domain.com',
            ...     directories=[1],
            ...     criticity_threshold=100,
            ...     description='test alert'
            ...     )

            Send test email notifier with input_type as attacks

            >>> tie.email_notifiers.create(
            ...     input_type='attacks',
            ...     attack_types=[1, 2],
            ...     profiles=[1],
            ...     address='test@domain.com',
            ...     directories=[1],
            ...     criticity_threshold=100,
            ...     description='test alert'
            ...     )
        '''
        partial = ('should_notify_on_initial_full_security_check', )
        if kwargs.get('input_type') == 'deviances':
            partial = partial + ('attack_types',)
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=partial))
        else:
            partial = partial + ('checkers',)
            payload = self._schema.dump(
                self._schema.load(kwargs, partial=partial))

        self._post("test-message", json=payload)
