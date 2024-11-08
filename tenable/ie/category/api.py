'''
Category
========

Methods described in this section relate to the category API.
These methods can be accessed at ``TenableIE.category``.

.. rst-class:: hide-signature
.. autoclass:: CategoryAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.category.schema import CategorySchema
from tenable.base.endpoint import APIEndpoint


class CategoryAPI(APIEndpoint):
    _path = 'categories'
    _schema = CategorySchema()

    def list(self) -> List[Dict]:
        '''
        Retrieves the list of categories in the instance.

        Returns:
            list:
                Returns a list of categories.

        Examples:

            >>> tie.category.list()
        '''
        return self._schema.load(self._get(), many=True)

    def details(self, category_id: str) -> Dict:
        '''
        Retrieves the details of particlar category bases on category_id.

        Args:
            category_id (str):
                The category instance identifier.

        Returns:
            dict:
                Returns the details of a given ``category_id``.

        Examples:

            >>> tie.category.details(category_id='5')
        '''
        return self._schema.load(self._get(f'{category_id}'))
