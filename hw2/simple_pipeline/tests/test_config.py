import tempfile
import yaml
from pathlib import Path
import pytest

from simple_pipeline.config import (
    ModelType,
    ModelConfig,
    TrainingConfig,
    LogisticRegressionConfig,
    RandomForestConfig,
    DecisionTreeConfig,
    load_config,
)


def test_model_type_enum():
    assert ModelType.LOGISTIC_REGRESSION == "logistic_regression"
    assert ModelType.RANDOM_FOREST == "random_forest"
    assert ModelType.DECISION_TREE == "decision_tree"


def test_model_config_defaults():
    config = ModelConfig()
    assert config.model_type == ModelType.LOGISTIC_REGRESSION
    assert config.random_state == 42
    assert config.test_size == 0.2


def test_model_config_custom():
    config = ModelConfig(
        model_type=ModelType.RANDOM_FOREST,
        random_state=123,
        test_size=0.3
    )
    assert config.model_type == ModelType.RANDOM_FOREST
    assert config.random_state == 123
    assert config.test_size == 0.3


def test_logistic_regression_config():
    config = LogisticRegressionConfig(max_iter=500, C=0.5)
    assert config.max_iter == 500
    assert config.C == 0.5


def test_random_forest_config():
    config = RandomForestConfig(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )
    assert config.n_estimators == 200
    assert config.max_depth == 10
    assert config.min_samples_split == 5
    assert config.min_samples_leaf == 2


def test_decision_tree_config():
    config = DecisionTreeConfig(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=3,
        criterion="entropy"
    )
    assert config.max_depth == 5
    assert config.min_samples_split == 10
    assert config.min_samples_leaf == 3
    assert config.criterion == "entropy"


def test_training_config_defaults():
    config = TrainingConfig()
    assert config.model.model_type == ModelType.LOGISTIC_REGRESSION
    assert isinstance(config.logistic_regression, LogisticRegressionConfig)
    assert isinstance(config.random_forest, RandomForestConfig)
    assert isinstance(config.decision_tree, DecisionTreeConfig)


def test_load_config_no_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nonexistent.yaml"
        config = load_config(config_path)
        assert isinstance(config, TrainingConfig)
        assert config.model.model_type == ModelType.LOGISTIC_REGRESSION


def test_load_config_with_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config_data = {
            "model": {
                "model_type": "random_forest",
                "random_state": 100,
                "test_size": 0.25
            },
            "random_forest": {
                "n_estimators": 150,
                "max_depth": 5
            }
        }
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f)

        config = load_config(config_path)
        assert config.model.model_type == ModelType.RANDOM_FOREST
        assert config.model.random_state == 100
        assert config.model.test_size == 0.25
        assert config.random_forest.n_estimators == 150
        assert config.random_forest.max_depth == 5


def test_training_config_validation():
    with pytest.raises(Exception):
        ModelConfig(test_size=1.5)

    with pytest.raises(Exception):
        ModelConfig(test_size=-0.1)

    with pytest.raises(Exception):
        LogisticRegressionConfig(C=-1.0)

