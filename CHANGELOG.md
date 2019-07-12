# Changelog
All notable changes to this project will be documented in this file.

## 0.x.x - 2019-xx-xx
### Added
- Authenticates by calling to `/company`

## 0.3.2 - 2019-07-11
### Added
- Use `prevedere_api.ini` in the installation directory to store the api_key
- Use `logging.exception` instead of printing exceptions
### Changed
- Improved error handling

## 0.3.1 - 2019-03-07
### Added
- Added arguments for:
    - `raw_model`: `as_of_date` and `exclude_indicators`
    - `forecast`: `as_of_date`
    - `indicator_series`: `start_date` and `end_date`
### Changed
- HTTP errors now include server response.

## 0.3.0 - 2019-02-13
### Added
- Added new endpoints: `forecast`, `correlation`, and `workbench`.
### Changed
- Minor refactoring

## 0.2.0 - 2019-02-11
### Changed
- No longer requires Pandas. API calls return JSON formatted data.
- Added try/except clause for HTTP requests.

## 0.1.1 - 2018-11-29
### Added
- CHANGELOG.md
- requirements.txt
- type hinting

### Changed
- Syntax fixes for PEP compliance
- Refactored so that the API key is the default payload.

## 0.1 - 2018-11-19
### Added
- Initial release
