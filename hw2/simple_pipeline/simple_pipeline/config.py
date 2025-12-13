from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field


class ModelType(str, Enum):
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST = "random_forest"
    DECISION_TREE = "decision_tree"


class ModelConfig(BaseModel):
    model_type: ModelType = Field(default=ModelType.LOGISTIC_REGRESSION)
    random_state: int = Field(default=42)
    test_size: float = Field(default=0.2, ge=0.0, le=1.0)


class LogisticRegressionConfig(BaseModel):
    max_iter: int = Field(default=1000)
    C: float = Field(default=1.0, gt=0.0)


class RandomForestConfig(BaseModel):
    n_estimators: int = Field(default=100, gt=0)
    max_depth: int | None = Field(default=None, gt=0)
    min_samples_split: int = Field(default=2, gt=0)
    min_samples_leaf: int = Field(default=1, gt=0)


class DecisionTreeConfig(BaseModel):
    max_depth: int | None = Field(default=None, gt=0)
    min_samples_split: int = Field(default=2, gt=0)
    min_samples_leaf: int = Field(default=1, gt=0)
    criterion: str = Field(default="gini")


class TrainingConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    logistic_regression: LogisticRegressionConfig = Field(default_factory=LogisticRegressionConfig)
    random_forest: RandomForestConfig = Field(default_factory=RandomForestConfig)
    decision_tree: DecisionTreeConfig = Field(default_factory=DecisionTreeConfig)
    data_path: Path = Field(default=Path("data/raw/classification_dataset.csv"))
    model_output_path: Path = Field(default=Path("models/trained_model.pkl"))


def load_config(config_path: Path | None = None) -> TrainingConfig:
    if config_path is None:
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config.yaml"
    
    config_path = Path(config_path)
    
    if config_path.exists():
        import yaml
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)
        return TrainingConfig(**config_dict)
    else:
        return TrainingConfig()

