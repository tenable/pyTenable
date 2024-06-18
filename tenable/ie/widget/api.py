'''
Widget
=======

Methods described in this section relate to the widget API.
These methods can be accessed at ``TenableIE.widgets``.

.. rst-class:: hide-signature
.. autoclass:: WidgetsAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.widget.schema import WidgetSchema, WidgetOptionSchema
from tenable.base.endpoint import APIEndpoint


class WidgetsAPI(APIEndpoint):
    _path = 'dashboards'
    _schema = WidgetSchema()

    def list(self, dashboard_id: int) -> List[Dict]:
        '''
        Retrieves all the widgets.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
        Returns:
            list:
                The list of widget objects.

        Examples:
            >>> tie.widgets.list(dashboard_id=13)
        '''
        return self._get(f"{dashboard_id}/widgets")

    def create(self,
               dashboard_id: int,
               pos_x: int,
               pos_y: int,
               width: int,
               height: int,
               title: str) -> List[Dict]:
        '''
        Creates a new widget.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            pos_x (int):
                x-axis position for widget.
            pos_y (int):
                y-axis position for widget.
            width (int):
                width of widget.
            height (int):
                height of widget.
            title (str):
                title for widget.

        Returns:
            list[dict]:
                The created widget object.

        Examples:
            >>> tie.widgets.create(
            ...     dashboard_id=1,
            ...     pos_x=1,
            ...     pos_y=1,
            ...     width=2,
            ...     height=2,
            ...     title='ExampleWidget',
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'posX': pos_x,
            'posY': pos_y,
            'width': width,
            'height': height,
            'title': title
        }))
        return self._schema.load(self._post(f'{dashboard_id}/widgets',
                                            json=payload))

    def details(self,
                dashboard_id: int,
                widget_id: int) -> Dict:
        '''
        Retrieves the details for a specific widget.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            widget_id (int):
                The widget instance identifier

        Returns:
            dict:
                The widget object.

        Examples:
            >>> tie.widget.details(dashboard_id=1, widget_id=1)
        '''
        return self._schema.load(self._get(f"{dashboard_id}"
                                           f"/widgets/{widget_id}"))

    def update(self,
               dashboard_id: int,
               widget_id: int,
               **kwargs) -> Dict:
        '''
        Updates an existing widget.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            widget_id (int):
                The dashboard instance identifier.
            pos_x (optional, int):
                x-axis position for widget.
            pos_y (optional, int):
                y-axis position for widget.
            width (optional, int):
                width of widget.
            height (optional, int):
                height of widget.
            title (optional, str):
                title for widget.

        Returns:
            dict:
                The updated widget object.

        Examples:
            >>> tie.widgets.update(
            ...     dashboard_id=1,
            ...     widget_id=1,
            ...     pos_x=1,
            ...     pos_y=1,
            ...     width=3,
            ...     height=3,
            ...     title='EditedWidget'
            ...     )
        '''
        payload = self._schema.dump(kwargs)
        return self._schema.load(self._patch(f"{dashboard_id}"
                                             f"/widgets/{widget_id}",
                                             json=payload))

    def delete(self,
               dashboard_id: int,
               widget_id: int) -> None:
        '''
        Deletes an existing widget.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            widget_id (int):
                The widget instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.widgets.delete(
            ...     dashboard_id=1,
            ...     widget_id=1
            ...     )
        '''
        self._delete(f"{dashboard_id}/widgets/{widget_id}")

    def widget_options_details(self,
                               dashboard_id: int,
                               widget_id: int) -> Dict:
        '''
        Gets the details of widget options.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            widget_id (int):
                The dashboard instance identifier.

        Returns:
            dict:
                The widget option object.

        Examples:
            >>> tie.widgets.widget_options_details(
            ...     widget_id=1,
            ...     dashboard_id=1
            ...     )
        '''
        schema = WidgetOptionSchema()
        return schema.load(self._get(f"{dashboard_id}/widgets/"
                                     f"{widget_id}/options"))

    def define_widget_options(self,
                              dashboard_id: int,
                              widget_id: int,
                              chart_type: str,
                              series: List[Dict]
                              ) -> None:
        '''
        Defines the widget option.

        Args:
            dashboard_id (int):
                The dashboard instance identifier.
            widget_id (int):
                The dashboard instance identifier.
            chart_type (str):
                The type of chart for widget. possible options
                 are ``BigNumber``, ``LineChart``, ``BarChart``,
                 ``SecurityCompliance`` and ``StepChart``.
            series (list):
                Additional keywords passed will be added to the series
                list of dicts within the API call.

        Returns:
            None:

        Examples:
            >>> tie.widgets.define_widget_options(
            ...     dashboard_id=1,
            ...     widget_id=1,
            ...     chart_type='BigNumber'
            ...     series=[
            ...     {
            ...         'dataOptions': {
            ...             'type': 'User',
            ...             'duration': 1,
            ...             'directoryIds': [1, 2, 3],
            ...             'active': True
            ...         },
            ...         'displayOptions': {
            ...             'label': 'label'
            ...         }
            ...     }
            ...     ]
            ...     )
        '''
        schema = WidgetOptionSchema()
        payload = schema.dump(schema.load({
            'type': chart_type,
            'series': list(series)
        }))

        self._put(f"{dashboard_id}/widgets/{widget_id}/options",
                  json=payload)
