"""
As exports are asynchronous, pyTenable by default will return an iterator to
handle the state tracking, data chunking, and presentation of the data in order
to reduce the amount of boilerplate code that would otherwise have to be
created.  These iterators support both serial iteration and threaded
handling of data depending on how the data is accessed.

.. autoclass:: WASExportsIterator
    :members:
"""
from typing import Optional, List, Dict, Any
from tenable.io.exports.iterator import ExportsIterator


class WASExportsIterator(ExportsIterator):
    def _get_status_resp(self) -> Dict:
        """
        Returns the status of current WAS export.
        """
        return self._api.was_exports.status(self.uuid)

    def cancel(self):
        """
        Cancels the current WAS export
        """
        self._api.was_exports.cancel(self.uuid)

    def _get_chunk_data(self, *args) -> List:
        """
        Private method. Downloads and returns chunk data.
        """
        return self._api.was_exports.download_chunk(args[1], args[2])
