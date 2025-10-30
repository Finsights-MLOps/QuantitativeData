"""Unit tests for helper functions."""
import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from utils.helpers import safe_div, setup_logger


class TestSafeDiv(unittest.TestCase):
    """Test cases for safe_div function."""

    def test_normal_division(self):
        """Test normal division."""
        self.assertEqual(safe_div(10, 2), 5.0)
        self.assertEqual(safe_div(100, 5), 20.0)

    def test_division_by_zero(self):
        """Test division by zero returns 0."""
        self.assertEqual(safe_div(10, 0), 0.0)
        self.assertEqual(safe_div(100, 0), 0.0)

    def test_zero_divided_by_number(self):
        """Test zero divided by number returns 0."""
        self.assertEqual(safe_div(0, 5), 0.0)
        self.assertEqual(safe_div(0, 100), 0.0)

    def test_none_values(self):
        """Test handling of None values."""
        self.assertEqual(safe_div(None, 5), 0.0)
        self.assertEqual(safe_div(10, None), 0.0)
        self.assertEqual(safe_div(None, None), 0.0)

    def test_nan_values(self):
        """Test handling of NaN values."""
        self.assertEqual(safe_div(float('nan'), 5), 0.0)
        self.assertEqual(safe_div(10, float('nan')), 0.0)
        self.assertEqual(safe_div(float('nan'), float('nan')), 0.0)

    def test_pandas_series_division(self):
        """Test division with pandas Series."""
        numerator = pd.Series([10, 20, 30])
        denominator = pd.Series([2, 5, 6])
        result = safe_div(numerator, denominator)
        
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 5.0)
        self.assertEqual(result[1], 4.0)
        self.assertEqual(result[2], 5.0)

    def test_pandas_series_with_zero(self):
        """Test pandas Series division with zero."""
        numerator = pd.Series([10, 20, 30])
        denominator = pd.Series([0, 5, 6])
        result = safe_div(numerator, denominator)
        
        self.assertTrue(pd.isna(result[0]))
        self.assertEqual(result[1], 4.0)
        self.assertEqual(result[2], 5.0)

    def test_pandas_series_with_inf(self):
        """Test pandas Series handling of infinity."""
        numerator = pd.Series([10, 20, 30])
        denominator = pd.Series([2, 0, 6])
        result = safe_div(numerator, denominator)
        
        # Check that inf values are replaced with NaN
        self.assertEqual(result[0], 5.0)
        self.assertTrue(pd.isna(result[1]))
        self.assertEqual(result[2], 5.0)


class TestSetupLogger(unittest.TestCase):
    """Test cases for setup_logger function."""

    def test_logger_creation(self):
        """Test logger is created successfully."""
        logger = setup_logger("test_logger", "test.log")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")

    def test_logger_has_handlers(self):
        """Test logger has handlers."""
        logger = setup_logger("test_logger", "test.log")
        self.assertGreater(len(logger.handlers), 0)

    def test_logger_level(self):
        """Test logger level."""
        logger = setup_logger("test_logger", "test.log", level=20)
        self.assertEqual(logger.level, 20)


if __name__ == '__main__':
    unittest.main()

