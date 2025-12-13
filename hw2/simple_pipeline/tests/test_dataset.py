import tempfile
from pathlib import Path
import pandas as pd
import pytest

from simple_pipeline.dataset import generate_classification_dataset


def test_generate_classification_dataset_default():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        X_df, y_series = generate_classification_dataset(output_dir=output_dir)

        assert isinstance(X_df, pd.DataFrame)
        assert isinstance(y_series, pd.Series)
        assert X_df.shape[0] == 1000
        assert X_df.shape[1] == 20
        assert len(y_series) == 1000
        assert y_series.name == "target"

        assert (output_dir / "classification_features.csv").exists()
        assert (output_dir / "classification_target.csv").exists()
        assert (output_dir / "classification_dataset.csv").exists()


def test_generate_classification_dataset_custom_params():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        X_df, y_series = generate_classification_dataset(
            n_samples=100,
            n_features=10,
            n_informative=5,
            n_redundant=2,
            n_classes=3,
            random_state=123,
            output_dir=output_dir
        )

        assert X_df.shape[0] == 100
        assert X_df.shape[1] == 10
        assert len(y_series) == 100
        assert set(y_series.unique()).issubset({0, 1, 2})


def test_generate_classification_dataset_files_created():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generate_classification_dataset(output_dir=output_dir)

        features_df = pd.read_csv(output_dir / "classification_features.csv")
        target_series = pd.read_csv(output_dir / "classification_target.csv")
        combined_df = pd.read_csv(output_dir / "classification_dataset.csv")

        assert features_df.shape[1] == 20
        assert "target" in target_series.columns
        assert "target" in combined_df.columns
        assert combined_df.shape[1] == 21


def test_generate_classification_dataset_reproducibility():
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
        output_dir1 = Path(tmpdir1)
        output_dir2 = Path(tmpdir2)

        X_df1, y_series1 = generate_classification_dataset(
            random_state=42, output_dir=output_dir1
        )
        X_df2, y_series2 = generate_classification_dataset(
            random_state=42, output_dir=output_dir2
        )

        pd.testing.assert_frame_equal(X_df1, X_df2)
        pd.testing.assert_series_equal(y_series1, y_series2)

