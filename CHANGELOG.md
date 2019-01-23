# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added Changelog and backfilled changes from 0.1.0 to current
- Added testing for user outputs #26
- Added testing for scanner outputs #30
- Added testing for permissions #34
- Added testing for groups #35
- Adjusted the doc format to no longer pin the sidebar #61

### Changed
- Launching a scan with alt_targets sends an array instead of a string #64
- Tenable.sc Analysis will now handle Query IDs #63
- Agent-Delete within Tenable.io Was using the wrong Endpoint #59


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



[Unreleased]: https://github.com/tenable/pyTenable/compare/0.3.8...master
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