from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib


def preprocess_data(
    raw_data_path: Path | str,
    output_path: Path | str | None = None,
    project_root: Path | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    raw_data_path = Path(raw_data_path)
    
    if not raw_data_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {raw_data_path}")
    
    df = pd.read_csv(raw_data_path)
    
    X = df.drop(columns=["target"])
    y = df["target"]
    
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns,
        index=X.index
    )
    
    processed_df = X_scaled.copy()
    processed_df["target"] = y
    
    if output_path is None:
        if project_root is None:
            project_root = Path(__file__).parent.parent
        output_path = project_root / "data" / "processed" / "classification_dataset.csv"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    processed_df.to_csv(output_path, index=False)
    
    scaler_path = output_path.parent / "scaler.pkl"
    joblib.dump(scaler, scaler_path)
    
    print(f"Preprocessed data saved to {output_path}")
    print(f"Scaler saved to {scaler_path}")
    print(f"  - Features shape: {X_scaled.shape}")
    print(f"  - Target shape: {y.shape}")
    
    return X_scaled, y

