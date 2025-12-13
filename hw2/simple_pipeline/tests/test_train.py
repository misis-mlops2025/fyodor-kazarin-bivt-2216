import tempfile
import joblib
from pathlib import Path
import pandas as pd
import pytest
from sklearn.datasets import make_classification

from simple_pipeline.config import ModelType, TrainingConfig, ModelConfig
from simple_pipeline.modeling.train import create_model, train_model


def test_create_model_logistic_regression():
    config = TrainingConfig(
        model=ModelConfig(model_type=ModelType.LOGISTIC_REGRESSION)
    )
    model = create_model(config)
    assert model.__class__.__name__ == "LogisticRegression"
    assert model.random_state == 42


def test_create_model_random_forest():
    from simple_pipeline.config import RandomForestConfig
    config = TrainingConfig(
        model=ModelConfig(model_type=ModelType.RANDOM_FOREST),
        random_forest=RandomForestConfig(n_estimators=50)
    )
    model = create_model(config)
    assert model.__class__.__name__ == "RandomForestClassifier"
    assert model.n_estimators == 50
    assert model.random_state == 42


def test_create_model_decision_tree():
    from simple_pipeline.config import DecisionTreeConfig
    config = TrainingConfig(
        model=ModelConfig(model_type=ModelType.DECISION_TREE),
        decision_tree=DecisionTreeConfig(max_depth=5)
    )
    model = create_model(config)
    assert model.__class__.__name__ == "DecisionTreeClassifier"
    assert model.max_depth == 5
    assert model.random_state == 42


def test_train_model_logistic_regression():
    with tempfile.TemporaryDirectory() as tmpdir:
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        df = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(10)])
        df["target"] = y

        data_path = Path(tmpdir) / "test_data.csv"
        model_path = Path(tmpdir) / "test_model.pkl"
        df.to_csv(data_path, index=False)

        config = TrainingConfig(
            model=ModelConfig(
                model_type=ModelType.LOGISTIC_REGRESSION,
                test_size=0.2
            ),
            data_path=data_path,
            model_output_path=model_path
        )

        model, accuracy = train_model(config)

        assert model.__class__.__name__ == "LogisticRegression"
        assert 0.0 <= accuracy <= 1.0
        assert model_path.exists()

        loaded_model = joblib.load(model_path)
        assert loaded_model.__class__.__name__ == "LogisticRegression"


def test_train_model_random_forest():
    from simple_pipeline.config import RandomForestConfig
    with tempfile.TemporaryDirectory() as tmpdir:
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        df = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(10)])
        df["target"] = y

        data_path = Path(tmpdir) / "test_data.csv"
        model_path = Path(tmpdir) / "test_model.pkl"
        df.to_csv(data_path, index=False)

        config = TrainingConfig(
            model=ModelConfig(
                model_type=ModelType.RANDOM_FOREST,
                test_size=0.3
            ),
            random_forest=RandomForestConfig(n_estimators=10),
            data_path=data_path,
            model_output_path=model_path
        )

        model, accuracy = train_model(config)

        assert model.__class__.__name__ == "RandomForestClassifier"
        assert 0.0 <= accuracy <= 1.0
        assert model_path.exists()


def test_train_model_decision_tree():
    from simple_pipeline.config import DecisionTreeConfig
    with tempfile.TemporaryDirectory() as tmpdir:
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        df = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(10)])
        df["target"] = y

        data_path = Path(tmpdir) / "test_data.csv"
        model_path = Path(tmpdir) / "test_model.pkl"
        df.to_csv(data_path, index=False)

        config = TrainingConfig(
            model=ModelConfig(model_type=ModelType.DECISION_TREE),
            decision_tree=DecisionTreeConfig(max_depth=3),
            data_path=data_path,
            model_output_path=model_path
        )

        model, accuracy = train_model(config)

        assert model.__class__.__name__ == "DecisionTreeClassifier"
        assert 0.0 <= accuracy <= 1.0
        assert model_path.exists()


def test_train_model_reproducibility():
    with tempfile.TemporaryDirectory() as tmpdir:
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        df = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(10)])
        df["target"] = y

        data_path = Path(tmpdir) / "test_data.csv"
        df.to_csv(data_path, index=False)

        config1 = TrainingConfig(
            model=ModelConfig(
                model_type=ModelType.LOGISTIC_REGRESSION,
                random_state=42
            ),
            data_path=data_path,
            model_output_path=Path(tmpdir) / "model1.pkl"
        )

        config2 = TrainingConfig(
            model=ModelConfig(
                model_type=ModelType.LOGISTIC_REGRESSION,
                random_state=42
            ),
            data_path=data_path,
            model_output_path=Path(tmpdir) / "model2.pkl"
        )

        _, accuracy1 = train_model(config1)
        _, accuracy2 = train_model(config2)

        assert accuracy1 == accuracy2
