# pyTenable

[![Documentation Status](https://readthedocs.org/projects/pytenable/badge/?version=latest)](http://pytenable.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/tenable/pyTenable.svg?branch=master)](https://travis-ci.org/tenable/pyTenable)
[![PyPI](https://img.shields.io/pypi/v/pytenable.svg)](https://pypi.org/project/pyTenable/)



pyTenable is a library designed to provide a simple & easy-to-understand library into the Tenable product APIs.  Currently the library is under active development and new componentry is being added & changed to fit the evolving needs, requirements, and desires for the end-goal of the library.

**WARNING:** Currently in a pre-alpha state and not suitable for general consumption yet.

For further documentation, please refer to the [online documentation](http://pytenable.readthedocs.io).

## TODO:

- _check should allow for passing a checking function for further validation.
  + Example would be validating filters.
- scans.create and scans.configure should have naturalization of all of the parameters mentioned in the api: https://cloud.tenable.com/api#/resources/scans/create
- scans module needs to be fully tested out.
- container_security needs to be fully tested out.
- SecurityCenter.analysis module needs to be completed to at least have parity with pySecurityCenter for full deprecation of pySC.
- The SecurityCenter library needs to be written based on the public API docs.
- A basic Nessus module needs to be written to handle authorization.
- 