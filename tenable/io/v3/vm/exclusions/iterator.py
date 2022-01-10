'''
Exlusions Iterator module
'''
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class ExclusionSearchIterator(SearchIterator):
    '''
    Exclusion search iterator
    '''
    pass


class ExclusionCSVIterator(CSVChunkIterator):
    '''
    Exclusion csv iterator
    '''
    pass
