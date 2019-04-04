# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added and tested out support for TenableSC RoleAPI #24

## [0.3.14]
### Fixed
- Corrected Doc Issue where the downloads API was incorrectly referencing sc.alerts
- Fixed issue with scan history deletion where the path was incorrect #101

## [0.3.13]
### Added
- Tested out TenableSC StatusAPI #22
- Tested out TenableSC SystemAPI #22
- Tested out TenableSC ScanZoneAPI #21
- Tested out TenableSC ScannerAPI #21
- Tested out Downloads API

### Fixed
- RetryError no longer itself throws an error due to logging.
- Fixed type mismatch bug in IO workbench filters #97
- Corrected issue with ScanZone updates using the wrong HTTP method #95
- Corrected doc issue with ScanResultAPI.export not referring to the fact that the exported scan is zipped.
- Corrected the raw HTTP method docs


## [0.3.12]
### Added
- Added view parameter for TenableSC.analysis.scan #73
- Added accept_risks module #18 (untested)
- Added system module and converted the TenableSC motule to use it over a raw call #22
- Added status module #22 (untested)

### Fixed
- Fixed issue with TenableSC.analysis.scan not properly passing a view. #73

## [0.3.11]
### Added
- Added proxy support for the IO, SC, etc. #72

### Fixed
- Fixed issue where supplied sessions weren't being properly passed to _build_session.

## [0.3.10]
### Added
- Added example for Workbench CSV Downloads for IO
- Added support for multi-value filters in IO.
- Added Request-UUID logging for all responses when available.
- Added TenableSC scan_instances endpoints and associated tests #19.
- Added TenableSC scan policies endpoints and associated tests #20.
- TenableIO can now pull API keys directly from environment variables as well.
- Added doc page detailing how to run the tests.
- Added TenableSC repositories endpoint and associated tests #17

### Fixed
- Exports methods in TenableIO now respect 0 integers being passed #69.
- Errored scan exports in TenableIO will no longer wait forever.
- Scan Exports using multiple chapters now works as expected #71 #70

### Removed
- schedule_* parameters in scans have been removed in favor of direct checking
    and documentation of the schedule dictionary.  This has larger implications
    down the line with repositories, alerts, etc.


## [0.3.9]
### Added
- Added the `aggregate` parameter for scan import.
- Added Changelog and backfilled changes from 0.1.0 to current
- Added testing for user outputs #26
- Added testing for scanner outputs #30
- Added testing for permissions #34
- Added testing for groups #35
- Adjusted the doc format to no longer pin the sidebar #61
- Added redaction to sensitive pathways #66
- Added tagging support #44

### Changed
- Tenable.sc files module was incorrectly pointing to self.post instead of self._api.post
- Launching a scan with alt_targets sends an array instead of a string #64
- Tenable.sc Analysis will now handle Query IDs #63
- Agent-Delete within Tenable.io Was using the wrong Endpoint #59
- Refactored TIOIterator to use less code when subclassing.
- Documented iterators and other common models.


## [0.3.8]
### Added
- Added TioExportsError to handle status error
- Tagging support for asset export


## [0.3.7]
### Added
- Added scans.status in Tenable.sc
- Added scans module for Tenable.sc
- Added logging support for the whole of pyTenable

### Changed
- Corrected pathway to acceptRiskRule for Tenable.sc package
- Scans.update renamed to Scans.edit in Tenable.io

### Removed
- analysis_type from being sent to the API


## [0.3.6]
### Added
- Tenable.sc login testing
- Tenable.sc Analysis testing #10

### Changed
- Fixed iterator looping issue
- Travis now runs all tests
- Converted pytest to use conftest standard
- Improved VCRpy testing

### Removed
- Container Security v1 tests (not VCRed)


## [0.3.5]
### Changed
- Fixed iterator first page problem
- Adjusted Tenable.sc model constructors to all behave the same uniform way


## [0.3.4]
### Added
- Added tagging support for vulnerability export
- Added VCRpy to all unit tests
- Added accept_risks Model to TenableSC

### Changed
- Moved get_status checking for iterators to conform to DRY
- lxml is now an optional dependency


## [0.3.3]
### Added
- Added scan_instances to TenableSC

### Changed
- tio.scanners.linking_key is now a method instead fo a property

### Removed
- Removed a lot of stubbed models that haven't been worked on yet


## [0.3.2]
### Changed
- Documentation refactored
- Mocked up some of the libraries for improved testing
- Fixed typo bug in sc.scans


## [0.3.1]
### Added
- Documented asset_activity to TenableIO

### Changed
- Re-pointed all SecurityCenter references to TenableSC instead
- Refactored schedule sub-document creation into a separate constructor for re-use
- Documentation improvements


## [0.3.0]
### Added
- Added unit tests for Inputs & Outputs for IO Scanner Groups
- Added unit tests for Inputs & Outputs for IO Policies
- Added unit tests for Inputs & Outputs for IO Plugins
- Added unit tests for Inputs & Outputs for IO Folders
- Added unit tests for Inputs & Outputs for IO Filters
- Added unit tests for Inputs & Outputs for IO Asset Lists
- Added unit tests for Inputs & Outputs for IO Target Groups
- Added unit tests for Inputs & Outputs for IO Sessions
- Added RetryError

### Changed
- Inlined all of the Documentation into the code itself
- Documentation refactoring effort for the whole package
- Unit test improvements


## [0.2.2]
### Changed
- Refactored long-description to better suit PyPI inclusion

## [0.2.1]
### Changed
- Inlined the Readme


## [0.2.0]
### Added
- Added TenableSC Analysis Model
- Added TenableSC Feeds Model
- Added TenableSC Files Model
- Added NessusReportv2 Model

### Changed
- Refactored the sub-package pathing
- Modified importing to be relative


## [0.1.0]
### Added
- Added TenableIO Exports Model
- Added TenableIO Scans Model
- Added

### Changed
- Fixed Time Conversion Issue #6



[Unreleased]: https://github.com/tenable/pyTenable/compare/0.3.14...master
[0.3.14]: https://github.com/tenable/pyTenable/compare/0.3.13...0.3.14
[0.3.13]: https://github.com/tenable/pyTenable/compare/0.3.12...0.3.13
[0.3.12]: https://github.com/tenable/pyTenable/compare/0.3.11...0.3.12
[0.3.11]: https://github.com/tenable/pyTenable/compare/0.3.10...0.3.11
[0.3.10]: https://github.com/tenable/pyTenable/compare/0.3.9...0.3.10
[0.3.9]: https://github.com/tenable/pyTenable/compare/0.3.8...0.3.9
[0.3.8]: https://github.com/tenable/pyTenable/compare/0.3.7...0.3.8
[0.3.7]: https://github.com/tenable/pyTenable/compare/0.3.6...0.3.7
[0.3.6]: https://github.com/tenable/pyTenable/compare/0.3.5...0.3.6
[0.3.5]: https://github.com/tenable/pyTenable/compare/0.3.4...0.3.5
[0.3.4]: https://github.com/tenable/pyTenable/compare/0.3.3...0.3.4
[0.3.3]: https://github.com/tenable/pyTenable/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/tenable/pyTenable/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/tenable/pyTenable/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/tenable/pyTenable/compare/0.2.2...0.3.0
[0.2.2]: https://github.com/tenable/pyTenable/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/tenable/pyTenable/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/tenable/pyTenable/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/tenable/pyTenable/compare/4ab62c61c80768a36b65ba5accef0bfe1350480e...0.1.0