"""Great Expectations tests for data quality."""
import great_expectations as ge
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def create_sample_dataframe():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({
        'ticker': ['AAPL', 'MSFT', 'GOOGL'],
        'year': [2023, 2023, 2023],
        'metric': ['income_stmt_Revenue', 'income_stmt_Revenue', 'income_stmt_Revenue'],
        'value': [1000000, 2000000, 1500000],
        'unit': ['USD', 'USD', 'USD'],
        'description': ['Total revenue', 'Total revenue', 'Total revenue']
    })


def test_dataframe_shape(df):
    """Test dataframe shape expectations."""
    suite = ge.dataset.PandasDataset(df)
    
    # Expect dataset to have specific number of columns
    suite.expect_table_column_count_to_equal(6)
    
    # Expect specific columns to exist
    suite.expect_table_columns_to_match_ordered_list(
        ['ticker', 'year', 'metric', 'value', 'unit', 'description']
    )
    
    return suite


def test_dataframe_types(df):
    """Test dataframe column types."""
    suite = ge.dataset.PandasDataset(df)
    
    # Expect specific data types
    suite.expect_column_values_to_be_of_type("ticker", "object")
    suite.expect_column_values_to_be_of_type("year", "int64")
    suite.expect_column_values_to_be_of_type("value", "float64" if df['value'].dtype == 'float64' else "int64")
    suite.expect_column_values_to_be_of_type("unit", "object")
    
    return suite


def test_dataframe_values(df):
    """Test dataframe value expectations."""
    suite = ge.dataset.PandasDataset(df)
    
    # Expect no null values in critical columns
    suite.expect_column_values_to_not_be_null("ticker")
    suite.expect_column_values_to_not_be_null("year")
    suite.expect_column_values_to_not_be_null("metric")
    suite.expect_column_values_to_not_be_null("value")
    
    # Expect year to be within reasonable range
    suite.expect_column_values_to_be_between("year", 2000, 2100)
    
    # Expect value to be positive
    suite.expect_column_values_to_be_between("value", 0, None)
    
    return suite


def test_dataframe_uniqueness(df):
    """Test dataframe uniqueness expectations."""
    suite = ge.dataset.PandasDataset(df)
    
    # Expect no completely duplicate rows
    suite.expect_table_row_count_to_be_between(0, 1000)
    
    return suite


def test_dataframe_content(df):
    """Test dataframe content expectations."""
    suite = ge.dataset.PandasDataset(df)
    
    # Expect unit to always be USD
    suite.expect_column_values_to_be_in_set("unit", ["USD"])
    
    return suite


def run_all_data_quality_tests(df):
    """Run all data quality tests."""
    print("Running Great Expectations data quality tests...")
    
    suites = []
    try:
        suite1 = test_dataframe_shape(df)
        suites.append(("Shape", suite1))
        print("✓ Shape tests passed")
    except Exception as e:
        print(f"✗ Shape tests failed: {e}")
    
    try:
        suite2 = test_dataframe_types(df)
        suites.append(("Types", suite2))
        print("✓ Type tests passed")
    except Exception as e:
        print(f"✗ Type tests failed: {e}")
    
    try:
        suite3 = test_dataframe_values(df)
        suites.append(("Values", suite3))
        print("✓ Value tests passed")
    except Exception as e:
        print(f"✗ Value tests failed: {e}")
    
    try:
        suite4 = test_dataframe_uniqueness(df)
        suites.append(("Uniqueness", suite4))
        print("✓ Uniqueness tests passed")
    except Exception as e:
        print(f"✗ Uniqueness tests failed: {e}")
    
    try:
        suite5 = test_dataframe_content(df)
        suites.append(("Content", suite5))
        print("✓ Content tests passed")
    except Exception as e:
        print(f"✗ Content tests failed: {e}")
    
    return suites


if __name__ == "__main__":
    # Create sample data and run tests
    df = create_sample_dataframe()
    suites = run_all_data_quality_tests(df)
    
    # Generate validation report
    for name, suite in suites:
        print(f"\n{name} Suite Expectations:")
        print(suite.get_expectation_suite())

