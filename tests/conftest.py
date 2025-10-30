"""Pytest configuration and fixtures."""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_company_facts():
    """Sample company facts data for testing."""
    return {
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "units": {
                        "USD": [
                            {"val": 1000000, "fy": 2023, "fp": "FY", "form": "10-K"},
                            {"val": 950000, "fy": 2022, "fp": "FY", "form": "10-K"}
                        ]
                    }
                },
                "NetIncomeLoss": {
                    "units": {
                        "USD": [
                            {"val": 100000, "fy": 2023, "fp": "FY", "form": "10-K"},
                            {"val": 90000, "fy": 2022, "fp": "FY", "form": "10-K"}
                        ]
                    }
                },
                "Assets": {
                    "units": {
                        "USD": [
                            {"val": 5000000, "fy": 2023, "fp": "FY", "form": "10-K"},
                            {"val": 4800000, "fy": 2022, "fp": "FY", "form": "10-K"}
                        ]
                    }
                },
                "GrossProfit": {
                    "units": {
                        "USD": [
                            {"val": 400000, "fy": 2023, "fp": "FY", "form": "10-K"},
                            {"val": 380000, "fy": 2022, "fp": "FY", "form": "10-K"}
                        ]
                    }
                }
            }
        }
    }


@pytest.fixture
def sample_dataframe():
    """Sample dataframe for testing."""
    return pd.DataFrame({
        'ticker': ['AAPL', 'MSFT', 'GOOGL'],
        'year': [2023, 2023, 2023],
        'metric': ['income_stmt_Revenue', 'income_stmt_Revenue', 'income_stmt_Revenue'],
        'value': [1000000, 2000000, 1500000],
        'unit': ['USD', 'USD', 'USD'],
        'description': ['Total revenue', 'Total revenue', 'Total revenue']
    })


@pytest.fixture
def mock_edgar_client():
    """Mock EdgarClient for testing."""
    mock = Mock()
    mock.get_company_facts.return_value = {
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "units": {
                        "USD": [
                            {"val": 1000000, "fy": 2023, "fp": "FY", "form": "10-K"}
                        ]
                    }
                }
            }
        }
    }
    return mock


@pytest.fixture
def mock_s3_client():
    """Mock boto3 S3 client for testing."""
    mock = Mock()
    mock.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    return mock


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    return Mock()


@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "USER_AGENT": "Test Agent (test@test.com)",
        "AWS_PROFILE": "test-profile",
        "S3_BUCKET": "test-bucket",
        "S3_FOLDER": "test-folder"
    }
