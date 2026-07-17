# pyTenable SDK

## Purpose

A Python SDK to interact with the various Tenable platform APIs.

## Key Files

|       Filename | Description                      |
| -------------: | :------------------------------- |
|       Justfile | Testing and validation pipelines |
| pyproject.toml | Python Project file              |
|  codebook.toml | Additional Wordlist for codebook |

## Subdirectories

|          Directory | Purpose                                               |
| -----------------: | :---------------------------------------------------- |
|              docs/ | Sphinx Documentation Files for the project            |
|          examples/ | Example scripts using the SDK                         |
|           tenable/ | Project sourcecode.                                   |
|         tenable/io | Legacy Tenable Vulnerability Management Package       |
|         tenable/sc | Legacy Tenable Security Center Package                |
|        tenable/apa | Legacy Tenable Attack Path Analysis Package           |
|        tenable/asm | Legacy Tenable Attack Surface Management Package      |
|         tenable/dl | Legacy Tenable Downloads Portal Package               |
|         tenable/ie | Legacy Tenable Identity Management Package            |
|     tenable/nessus | Legacy Tenable Nessus Package                         |
|         tenable/ot | Legacy Tenable OT Security Package                    |
|     teable/reports | Legacy Tenable Report Parser                          |
| tenable/tenableone | Legacy Tenable One Package                            |
|             tests/ | pytest testing framework.                             |
|      tenable/cloud | Development Package for ASM, APA, IO, and Tenable One |

## For AI Agents

### Working in this directory:

- Python 3.12 compatibility is required.
- Data validation and serialization happens through pydantic models.
- Modules must be written to support both sync and async code.
- Modules must be written following expected patterns already defined.
- Listing methods should use the `get()` method name.
- Fetching individual Items from the API should use the `details()` method name.
- Any fixes in any of the legacy packages should be as minimal as possible. Do not rewrite the entire module.

### Working with Tenable Cloud APIs:

- [Platform & Settings OpenAPI Schema](https://developer.tenable.com/openapi/tenable-platform-settings.json)
- [Vulnerability Management OpenAPI Schema](https://developer.tenable.com/openapi/vulnerability-management.json)
- [Web Application Security OpenAPI Schema](https://developer.tenable.com/openapi/web-app-scanning.json)
- [Exposure Management OpenAPI Schema](https://developer.tenable.com/openapi/exposure-management.json)
- [PCI ASV OpenAPI Schema](https://developer.tenable.com/openapi/pci-asv.json)
- [MSSP Portal OpenAPI Schema](https://developer.tenable.com/openapi/mssp.json)
- [Identity Exposure OpenAPI Schema](https://developer.tenable.com/openapi/identity-exposure.json)
- [Attack Surface Management OpenAPI Schema](https://developer.tenable.com/openapi/attack-surface-management.json)
- [Downloads Portal OpenAPI Schema](https://developer.tenable.com/openapi/attack-surface-management.json)

### Common Patterns

- Tenable Cloud package uses Pydantic v2 for data serialization and deserialization.
- Tenable Cloud package is written using the the RestFly version 2 package, which is located at `/Users/steve/Dropbox/Repositories/python_modules/restfly`.
- Tenable Cloud package uses a common models directory for models for a given part of the platform, and private modules for the API.
- Tenable Cloud API modules must be both sync and async.
- Tenable Cloud API modules inherit from restfly's `APIEndpoint` and `AsyncAPIEndpoint` classes.
- Tenable Cloud Pagination iterators use restfly's `APIIterator`.

### Testing

- Testing is performed through pytest.
- API Testing is done using the `pytest-httpx` package.
- To run the tests, use `uv run --isolated --group dev pytest`
