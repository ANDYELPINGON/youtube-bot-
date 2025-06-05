# YouTube Bot

This repository contains YouTube automation scripts.

## Files

- `main.py` - Basic YouTube view simulator using Selenium
- `bo.py` - Advanced view bot with Selenium and Playwright support
- `proxy_rotation.py` - Simple proxy rotation utility

## Testing

The project now includes comprehensive unit tests to ensure code quality and reliability.

### Test Structure

- `tests/` - Test directory
- `tests/test_main.py` - Tests for main.py functionality
- `tests/test_bo.py` - Tests for bo.py classes and methods
- `tests/test_proxy_rotation.py` - Tests for proxy rotation utility

### Running Tests

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
python -m pytest
```

Run tests with verbose output:
```bash
python -m pytest -v
```

Run specific test file:
```bash
python -m pytest tests/test_main.py
```

### Test Coverage

The test suite covers:
- Configuration validation
- Driver setup and error handling
- Chrome options configuration
- Directory creation logic
- View simulation logic (mocked to avoid actual browser automation)
- Proxy rotation functionality
- Human behavior simulation classes
- Error handling and edge cases

All tests use mocking to avoid dependencies on external services or browser automation during testing.

### Test Statistics

- **Total Tests**: 22
- **Test Files**: 3
- **Coverage**: Core functionality and error handling paths