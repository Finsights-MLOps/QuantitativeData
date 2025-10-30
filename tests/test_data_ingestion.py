"""Pytest tests for data ingestion functions."""
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from scripts import data_ingestion


class TestExtractCompanies:
    """Test cases for extract_companies function."""

    @patch('scripts.data_ingestion.requests.get')
    def test_extract_companies_success(self, mock_get):
        """Test successful extraction of companies."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            '0': {'ticker': 'AAPL', 'cik_str': '320193'},
            '1': {'ticker': 'MSFT', 'cik_str': '789019'},
            '2': {'ticker': 'GOOGL', 'cik_str': '1652044'}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = data_ingestion.extract_companies(n=2)
        
        assert isinstance(result, dict)
        assert len(result) == 2
        assert 'AAPL' in result
        assert result['AAPL'] == '0000320193'  # zfilled CIK

    @patch('scripts.data_ingestion.requests.get')
    def test_extract_companies_with_limit(self, mock_get):
        """Test extraction with limit parameter."""
        mock_response = Mock()
        mock_response.json.return_value = {
            '0': {'ticker': 'AAPL', 'cik_str': '320193'},
            '1': {'ticker': 'MSFT', 'cik_str': '789019'},
            '2': {'ticker': 'GOOGL', 'cik_str': '1652044'}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = data_ingestion.extract_companies(n=1)
        
        assert len(result) == 1

    @patch('scripts.data_ingestion.requests.get')
    def test_extract_companies_cik_formatting(self, mock_get):
        """Test CIK formatting with zero padding."""
        mock_response = Mock()
        mock_response.json.return_value = {
            '0': {'ticker': 'AAPL', 'cik_str': '320193'}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = data_ingestion.extract_companies(n=1)
        
        # Check CIK is zero-padded to 10 digits
        assert result['AAPL'] == '0000320193'

    @patch('scripts.data_ingestion.requests.get')
    def test_extract_companies_request_error(self, mock_get):
        """Test handling of request errors."""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        with pytest.raises(requests.RequestException):
            data_ingestion.extract_companies(n=1)


class TestFetchRawFacts:
    """Test cases for fetch_raw_facts function."""

    @patch('scripts.data_ingestion.EdgarClient')
    def test_fetch_raw_facts_success(self, mock_client_class):
        """Test successful fetching of raw facts."""
        mock_client = Mock()
        mock_client.get_company_facts.return_value = {"facts": {"us-gaap": {}}}
        mock_client_class.return_value = mock_client

        result = data_ingestion.fetch_raw_facts('0000320193')
        
        assert result == {"facts": {"us-gaap": {}}}
        mock_client.get_company_facts.assert_called_once_with(cik='0000320193')

    @patch('scripts.data_ingestion.EdgarClient')
    def test_fetch_raw_facts_with_retries(self, mock_client_class):
        """Test retry mechanism on failure."""
        mock_client = Mock()
        # First two attempts fail, third succeeds
        mock_client.get_company_facts.side_effect = [
            Exception("Error 1"),
            Exception("Error 2"),
            {"facts": {"us-gaap": {}}}
        ]
        mock_client_class.return_value = mock_client

        result = data_ingestion.fetch_raw_facts('0000320193', retries=3)
        
        assert result == {"facts": {"us-gaap": {}}}
        assert mock_client.get_company_facts.call_count == 3

    @patch('scripts.data_ingestion.EdgarClient')
    @patch('scripts.data_ingestion.time.sleep')
    def test_fetch_raw_facts_all_retries_fail(self, mock_sleep, mock_client_class):
        """Test when all retries fail."""
        mock_client = Mock()
        mock_client.get_company_facts.side_effect = Exception("Error")
        mock_client_class.return_value = mock_client

        result = data_ingestion.fetch_raw_facts('0000320193', retries=2)
        
        assert result is None
        assert mock_client.get_company_facts.call_count == 2


@pytest.mark.slow
@pytest.mark.integration
class TestIngestData:
    """Integration tests for ingest_data function."""

    @patch('scripts.data_ingestion.extract_companies')
    @patch('scripts.data_ingestion.fetch_raw_facts')
    @patch('scripts.data_ingestion.time.sleep')
    def test_ingest_data_success(self, mock_sleep, mock_fetch, mock_extract):
        """Test successful data ingestion."""
        # Setup mocks
        mock_extract.return_value = {'AAPL': '0000320193'}
        mock_fetch.return_value = {"facts": {"us-gaap": {}}}
        
        result = data_ingestion.ingest_data(n=1)
        
        assert isinstance(result, dict)
        assert 'AAPL' in result
        mock_extract.assert_called_once_with(n=1)
        mock_fetch.assert_called_once()

    @patch('scripts.data_ingestion.extract_companies')
    @patch('scripts.data_ingestion.fetch_raw_facts')
    @patch('scripts.data_ingestion.time.sleep')
    def test_ingest_data_with_multiple_companies(self, mock_sleep, mock_fetch, mock_extract):
        """Test ingestion with multiple companies."""
        mock_extract.return_value = {
            'AAPL': '0000320193',
            'MSFT': '0000789019'
        }
        mock_fetch.return_value = {"facts": {"us-gaap": {}}}
        
        result = data_ingestion.ingest_data(n=2)
        
        assert len(result) == 2
        assert mock_fetch.call_count == 2

