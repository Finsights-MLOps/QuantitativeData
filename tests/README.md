# Testing Documentation

This directory contains comprehensive tests for the SEC 10-K Pipeline using pytest, unittest, and Great Expectations.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_helpers.py          # Unittest tests for helper functions
├── test_data_preprocessing.py  # Unittest tests for data preprocessing
├── test_data_ingestion.py   # Pytest tests for data ingestion
├── test_data_loading.py     # Pytest tests for data loading
└── test_data_quality.py     # Great Expectations data quality tests
```

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Run only unittest tests
python -m unittest discover tests -p "test_*.py" -v

# Run only pytest tests
pytest tests/test_data_ingestion.py -v
pytest tests/test_data_loading.py -v

# Run with coverage
pytest tests/ --cov=scripts --cov=utils --cov-report=html
```

### Run Great Expectations Tests

```bash
python tests/test_data_quality.py
```

### Run Tests with Markers

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration

# Skip slow tests
pytest tests/ -m "not slow"
```

## Test Types

### 1. Unit Tests (unittest)
- **Location**: `test_helpers.py`, `test_data_preprocessing.py`
- **Purpose**: Test individual functions and methods in isolation
- **Run**: `python -m unittest discover tests/`

### 2. Integration Tests (pytest)
- **Location**: `test_data_ingestion.py`, `test_data_loading.py`
- **Purpose**: Test interaction between components
- **Run**: `pytest tests/ -m integration`

### 3. Data Quality Tests (Great Expectations)
- **Location**: `test_data_quality.py`
- **Purpose**: Validate data structure, types, and quality
- **Run**: `python tests/test_data_quality.py`

## Test Coverage

View coverage report:
```bash
pytest --cov=scripts --cov=utils --cov-report=html
open htmlcov/index.html
```

## Pytest Markers

Available markers:
- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Tests that take longer to run
- `@pquit.mark.api` - Tests that make API calls

## Continuous Integration

Tests are designed to run in CI/CD pipelines. The `pytest.ini` configuration includes:
- Verbose output (-v)
- Coverage reporting
- Test discovery patterns
- Marker definitions

## Adding New Tests

### For Unittest:
```python
import unittest

class TestYourFunction(unittest.TestCase):
    def test_something(self):
        # Your test code
        self.assertEqual(result, expected)
```

### For Pytest:
```python
import pytest

def test_something():
    # Your test code
    assert result == expected
```

### For Great Expectations:
```python
import great_expectations as ge

def test_dataframe_expectation(df):
    suite = ge.dataset.PandasDataset(df)
    suite.expect_column_values_to_not_be_null("column_name")
    return suite
```

