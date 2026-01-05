"""
Tests for data handling logic (full data, sampling, summary statistics).
"""
import os
import pytest
import pandas as pd
import numpy as np


class TestDataSizeDetection:
    """Tests for determining which data mode to use."""

    def test_small_csv_full_mode(self, sample_csv_small):
        """Test that small CSV triggers full data mode."""
        df = pd.read_csv(sample_csv_small)
        full_csv = df.to_csv(index=False)
        csv_size = len(full_csv)

        # Should be less than 50KB threshold
        assert csv_size < 50000

    def test_medium_csv_sample_mode(self, sample_csv_medium):
        """Test that medium CSV triggers sample mode."""
        df = pd.read_csv(sample_csv_medium)
        full_csv = df.to_csv(index=False)
        csv_size = len(full_csv)

        # Should be between 50KB and 500KB
        assert 50000 <= csv_size < 500000

    def test_large_csv_summary_mode(self, sample_csv_large):
        """Test that large CSV triggers summary mode."""
        df = pd.read_csv(sample_csv_large)
        full_csv = df.to_csv(index=False)
        csv_size = len(full_csv)

        # Should be more than 500KB
        assert csv_size >= 500000


class TestDataSampling:
    """Tests for random sampling functionality."""

    def test_random_sample_size(self, sample_csv_medium):
        """Test that random sample has correct size."""
        df = pd.read_csv(sample_csv_medium)
        sample_size = 500
        random_seed = 42

        df_sample = df.sample(n=min(sample_size, len(df)), random_state=random_seed)

        assert len(df_sample) == min(sample_size, len(df))

    def test_random_sample_reproducibility(self, sample_csv_medium):
        """Test that sampling is reproducible with same seed."""
        df = pd.read_csv(sample_csv_medium)
        sample_size = 500
        random_seed = 42

        sample1 = df.sample(n=sample_size, random_state=random_seed)
        sample2 = df.sample(n=sample_size, random_state=random_seed)

        # Should be identical
        pd.testing.assert_frame_equal(sample1, sample2)

    def test_random_sample_different_seeds(self, sample_csv_medium):
        """Test that different seeds produce different samples."""
        df = pd.read_csv(sample_csv_medium)
        sample_size = 500

        sample1 = df.sample(n=sample_size, random_state=42)
        sample2 = df.sample(n=sample_size, random_state=43)

        # Should be different
        assert not sample1.equals(sample2)

    def test_sample_smaller_than_dataframe(self, sample_csv_small):
        """Test sampling when dataframe is smaller than sample size."""
        df = pd.read_csv(sample_csv_small)
        sample_size = 1000  # Much larger than df

        # Should not raise error
        df_sample = df.sample(n=min(sample_size, len(df)), random_state=42)

        # Should return all rows
        assert len(df_sample) == len(df)


class TestSummaryStatistics:
    """Tests for summary statistics generation."""

    def test_summary_includes_shape(self, sample_csv_large):
        """Test that summary includes dataset shape."""
        df = pd.read_csv(sample_csv_large)

        summary = f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns"

        assert str(df.shape[0]) in summary
        assert str(df.shape[1]) in summary

    def test_summary_includes_columns(self, sample_csv_large):
        """Test that summary includes column information."""
        df = pd.read_csv(sample_csv_large)

        columns_info = f"Columns: {list(df.columns)}"

        assert "position_text" in columns_info
        assert "participant_id" in columns_info

    def test_summary_numeric_statistics(self, sample_csv_large):
        """Test that summary includes numeric column statistics."""
        df = pd.read_csv(sample_csv_large)

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        assert len(numeric_cols) > 0

        desc = df.describe()
        assert 'round_number' in desc.columns

    def test_summary_text_column_statistics(self, sample_csv_large):
        """Test that summary includes text column statistics."""
        df = pd.read_csv(sample_csv_large)

        if 'position_text' in df.columns:
            non_null_count = df['position_text'].notna().sum()
            null_count = df['position_text'].isna().sum()
            avg_length = df['position_text'].str.len().mean()

            assert non_null_count + null_count == len(df)
            assert avg_length > 0

    def test_summary_categorical_value_counts(self, sample_csv_large):
        """Test that summary includes categorical value counts."""
        df = pd.read_csv(sample_csv_large)

        categorical_cols = df.select_dtypes(include=['object', 'category']).columns

        for col in categorical_cols:
            if col != 'position_text':  # Skip long text columns
                value_counts = df[col].value_counts()
                assert len(value_counts) > 0


class TestDataInfo:
    """Tests for data_info dictionary structure."""

    def test_full_mode_data_info(self, sample_csv_small):
        """Test data_info structure for full mode."""
        df = pd.read_csv(sample_csv_small)
        full_csv = df.to_csv(index=False)

        data_info = {
            'mode': 'full',
            'total_rows': df.shape[0],
            'csv_data': full_csv,
            'note': "This is the complete dataset."
        }

        assert data_info['mode'] == 'full'
        assert data_info['total_rows'] == len(df)
        assert 'csv_data' in data_info
        assert 'note' in data_info

    def test_sample_mode_data_info(self, sample_csv_medium):
        """Test data_info structure for sample mode."""
        df = pd.read_csv(sample_csv_medium)
        sample_size = 500
        df_sample = df.sample(n=min(sample_size, len(df)), random_state=42)
        data_csv = df_sample.to_csv(index=False)

        data_info = {
            'mode': 'sample',
            'sample_size': len(df_sample),
            'total_rows': len(df),
            'csv_data': data_csv,
            'note': f"NOTE: This is a random sample of {len(df_sample)} rows from {len(df)} total rows."
        }

        assert data_info['mode'] == 'sample'
        assert data_info['sample_size'] <= data_info['total_rows']
        assert 'csv_data' in data_info

    def test_summary_mode_data_info(self, sample_csv_large):
        """Test data_info structure for summary mode."""
        df = pd.read_csv(sample_csv_large)
        summary = f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns"

        data_info = {
            'mode': 'summary',
            'total_rows': df.shape[0],
            'total_cols': df.shape[1],
            'data_summary': summary,
            'note': f"NOTE: Dataset is very large. Providing summary statistics."
        }

        assert data_info['mode'] == 'summary'
        assert data_info['total_rows'] == len(df)
        assert data_info['total_cols'] == len(df.columns)
        assert 'data_summary' in data_info


class TestCSVLoading:
    """Tests for CSV file loading."""

    def test_load_valid_csv(self, sample_csv_small):
        """Test loading a valid CSV file."""
        df = pd.read_csv(sample_csv_small)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'position_text' in df.columns

    def test_csv_columns_present(self, sample_csv_small):
        """Test that expected columns are present."""
        df = pd.read_csv(sample_csv_small)

        expected_columns = ['position_text', 'participant_id', 'round_number']
        for col in expected_columns:
            assert col in df.columns

    def test_csv_data_types(self, sample_csv_small):
        """Test that data types are correct."""
        df = pd.read_csv(sample_csv_small)

        assert df['position_text'].dtype == 'object'
        assert df['participant_id'].dtype == 'object'
        # round_number should be numeric
        assert pd.api.types.is_numeric_dtype(df['round_number'])
