from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from simple_pipeline.config import ModelType, TrainingConfig, load_config


def create_model(config: TrainingConfig):
    model_type = config.model.model_type

    if model_type == ModelType.LOGISTIC_REGRESSION:
        lr_config = config.logistic_regression
        return LogisticRegression(
            max_iter=lr_config.max_iter,
            C=lr_config.C,
            random_state=config.model.random_state,
        )
    if model_type == ModelType.RANDOM_FOREST:
        rf_config = config.random_forest
        return RandomForestClassifier(
            n_estimators=rf_config.n_estimators,
            max_depth=rf_config.max_depth,
            min_samples_split=rf_config.min_samples_split,
            min_samples_leaf=rf_config.min_samples_leaf,
            random_state=config.model.random_state,
        )
    if model_type == ModelType.DECISION_TREE:
        dt_config = config.decision_tree
        return DecisionTreeClassifier(
            max_depth=dt_config.max_depth,
            min_samples_split=dt_config.min_samples_split,
            min_samples_leaf=dt_config.min_samples_leaf,
            criterion=dt_config.criterion,
            random_state=config.model.random_state,
        )
    raise ValueError(f"Unknown model type: {model_type}")


def train_model(config: TrainingConfig | None = None):
    if config is None:
        config = load_config()

    project_root = Path(__file__).parent.parent.parent

    if config.data_path.is_absolute():
        data_path = config.data_path
    else:
        data_path = project_root / config.data_path

    df = pd.read_csv(data_path)

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.model.test_size, random_state=config.model.random_state
    )

    model = create_model(config)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    print(f"Model: {config.model.model_type.value}")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    if config.model_output_path.is_absolute():
        model_output_path = config.model_output_path
    else:
        model_output_path = project_root / config.model_output_path

    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f"\nModel saved to {model_output_path}")

    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "model_type": config.model.model_type.value
    }

    metrics_path = project_root / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return model, accuracy


if __name__ == "__main__":
    train_model()
