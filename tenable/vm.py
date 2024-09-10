"""
Temporary shim to allow folkd to import the TenableIO module as TenableVM
as well.  Eventually we need to migrate the io sub-pkg to vm and reverse this
shim for backwards compatability.
"""
from .io import TenableIO as TenableVM
