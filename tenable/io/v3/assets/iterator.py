'''
Asset Iterator module
'''
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class AssetSearchIterator(SearchIterator):
    '''
    Asset search iterator
    '''
    pass


class AssetCSVIterator(CSVChunkIterator):
    '''
    Asset csv iterator
    '''
    pass
