from pathlib import Path
import pandas as pd
from sklearn.datasets import make_classification


def generate_classification_dataset(
    n_samples: int = 1000,
    n_features: int = 20,
    n_informative: int = 10,
    n_redundant: int = 5,
    n_classes: int = 2,
    random_state: int = 42,
    output_dir: Path | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_classes=n_classes,
        random_state=random_state,
    )

    feature_names = [f"feature_{i+1}" for i in range(n_features)]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_series = pd.Series(y, name="target")

    if output_dir is None:
        project_root = Path(__file__).parent.parent
        output_dir = project_root / "data" / "raw"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    X_df.to_csv(output_dir / "classification_features.csv", index=False)
    y_series.to_csv(output_dir / "classification_target.csv", index=False)

    combined_df = X_df.copy()
    combined_df["target"] = y_series
    combined_df.to_csv(output_dir / "classification_dataset.csv", index=False)

    print(f"Dataset saved to {output_dir}")
    print(f"  - Features shape: {X_df.shape}")
    print(f"  - Target shape: {y_series.shape}")
    print(f"  - Classes: {n_classes}")

    return X_df, y_series


if __name__ == "__main__":
    generate_classification_dataset()
