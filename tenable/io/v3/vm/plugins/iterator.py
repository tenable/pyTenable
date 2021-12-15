from tenable.io.base import TIOIterator


class PluginIterator(TIOIterator):
    """
    The plugins iterator provides a scalable way to work through plugin result
    sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information
    and then continue to return records from the next page
    (and the next, and the next) until the counter reaches the total
    number of records that the API has reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
        populate_maptable (bool):
            Informs the iterator whether to construct the plugin to family maps
            for injecting the plugin family data into each item.
    """
    _maptable = None
    populate_maptable = False

    def _populate_family_cache(self):
        """
        Generates the maptable to use to graft on the plugin family information
        to the plugins. Effectively what we doing is generating a dictionary of
        2 subdictionaries.  Each one of these is a simple hash table allowing
        the iterator to resolve the name of the family by ID and the family ID
        by the plugin membership.  This information is currently lacking in the
        plugin listing output and was requested by a customer.

        .. note::
            This currently seems to add about 7-10 seconds before the first
            item is returned, as it seems to take this long to generate the
            data. We can focus on reducing this time later on with the
            introduction of multi-threaded iterators && async API calls.
        """
        self._maptable = {
            'plugins': dict(),
            'families': dict()
        }
        for family in self._api.plugins.families():
            self._maptable['families'][family['id']] = family['name']

        for fam_id in self._maptable['families'].keys():
            for plugin in self._api.plugins.family_details(fam_id)['plugins']:
                self._maptable['plugins'][plugin['id']] = fam_id

    def next(self):
        item = super(PluginIterator, self).next()

        # If the populate_maptable flag is set,
        # then we will build the mappings.
        if not self._maptable and self.populate_maptable:
            self._populate_family_cache()

        # If the maptable exists, then graft on the plugin family information
        # on to to the item.
        if self._maptable:
            try:
                fid = self._maptable['plugins'][item['id']]
                item['family_id'] = fid
                item['family_name'] = self._maptable['families'][fid]
            except KeyError:
                self._log.warning(
                    f"plugin id {item['id']} not found in plugin family"
                )
                item['family_id'] = None
                item['family_name'] = None
        return item
