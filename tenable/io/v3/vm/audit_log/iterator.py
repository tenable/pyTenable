'''
Audit Log Iterator module
'''
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class AuditLogSearchIterator(SearchIterator):
    '''
    Audit Log search iterator
    '''


class AuditLogCSVIterator(CSVChunkIterator):
    '''
    Audit Log csv iterator
    '''
