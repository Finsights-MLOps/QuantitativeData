"""Pytest tests for data loading functions."""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from scripts import data_loading


class TestSaveToS3:
    """Test cases for save_to_s3 function."""

    @patch('scripts.data_loading.boto3.session.Session')
    def test_save_to_s3_success(self, mock_session_class):
        """Test successful S3 upload."""
        # Setup mocks
        mock_session = Mock()
        mock_s3_client = Mock()
        mock_s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        mock_session.client.return_value = mock_s3_client
        mock_session_class.return_value = mock_session
        
        test_data = [
            {"ticker": "AAPL", "year": 2023, "value": 1000000}
        ]
        
        result = data_loading.save_to_s3(test_data)
        
        # Verify S3 put_object was called
        mock_s3_client.put_object.assert_called_once()
        call_kwargs = mock_s3_client.put_object.call_args[1]
        
        assert "Bucket" in call_kwargs
        assert "Key" in call_kwargs
        assert "Body" in call_kwargs
        assert "ContentType" in call_kwargs
        assert call_kwargs["ContentType"] == "application/json"

    @patch('scripts.data_loading.boto3.session.Session')
    def test_save_to_s3_json_serialization(self, mock_session_class):
        """Test that data is properly JSON serialized."""
        mock_session = Mock()
        mock_s3_client = Mock()
        mock_s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        mock_session.client.return_value = mock_s3_client
        mock_session_class.return_value = mock_session
        
        test_data = [{"key": "value"}]
        
        data_loading.save_to_s3(test_data)
        
        # Verify data is JSON serialized
        call_kwargs = mock_s3_client.put_object.call_args[1]
        body = call_kwargs["Body"]
        
        # Body should be bytes
        assert isinstance(body, bytes)
        
        # Can deserialize to JSON
        deserialized = json.loads(body.decode("utf-8"))
        assert deserialized == test_data

    @patch('scripts.data_loading.boto3.session.Session')
    def test_save_to_s3_with_empty_data(self, mock_session_class):
        """Test S3 upload with empty data."""
        mock_session = Mock()
        mock_s3_client = Mock()
        mock_s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        mock_session.client.return_value = mock_s3_client
        mock_session_class.return_value = mock_session
        
        result = data_loading.save_to_s3([])
        
        # Should still upload empty list
        mock_s3_client.put_object.assert_called_once()

    @patch('scripts.data_loading.boto3.session.Session')
    def test_save_to_s3_error_handling(self, mock_session_class):
        """Test error handling in S3 upload."""
        mock_session = Mock()
        mock_s3_client = Mock()
        mock_s3_client.put_object.side_effect = Exception("S3 error")
        mock_session.client.return_value = mock_s3_client
        mock_session_class.return_value = mock_session
        
        test_data = [{"key": "value"}]
        
        # Should raise the exception
        with pytest.raises(Exception, match="S3 error"):
            data_loading.save_to_s3(test_data)

