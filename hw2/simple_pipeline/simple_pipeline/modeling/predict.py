from pathlib import Path
import joblib
import pandas as pd
from datetime import datetime


def load_model_and_scaler(
    model_path: Path | str,
    scaler_path: Path | str | None = None,
    project_root: Path | None = None,
):
    model_path = Path(model_path)
    
    if not model_path.is_absolute():
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        model_path = project_root / model_path
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    model = joblib.load(model_path)
    
    if scaler_path is None:
        scaler_path = model_path.parent.parent / "data" / "processed" / "scaler.pkl"
    else:
        scaler_path = Path(scaler_path)
    
    if not scaler_path.is_absolute():
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        scaler_path = project_root / scaler_path
    
    scaler = None
    if scaler_path.exists():
        scaler = joblib.load(scaler_path)
    
    return model, scaler


def predict_batch(
    data_path: Path | str,
    model_path: Path | str,
    output_path: Path | str | None = None,
    scaler_path: Path | str | None = None,
    project_root: Path | None = None,
) -> pd.DataFrame:
    data_path = Path(data_path)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    if project_root is None:
        project_root = Path("/opt/airflow")
    
    model, scaler = load_model_and_scaler(
        model_path=model_path,
        scaler_path=scaler_path,
        project_root=project_root,
    )
    
    df = pd.read_csv(data_path)
    
    if "target" in df.columns:
        X = df.drop(columns=["target"])
    else:
        X = df
    
    if scaler is not None:
        X_scaled = scaler.transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    predictions = model.predict(X)
    prediction_proba = None
    if hasattr(model, "predict_proba"):
        prediction_proba = model.predict_proba(X)
    
    results_df = df.copy()
    results_df["prediction"] = predictions
    
    if prediction_proba is not None:
        for i in range(prediction_proba.shape[1]):
            results_df[f"probability_class_{i}"] = prediction_proba[:, i]
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = project_root / "data" / "predictions" / f"predictions_{timestamp}.csv"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    
    print(f"Predictions saved to {output_path}")
    print(f"  - Total predictions: {len(predictions)}")
    print(f"  - Unique predictions: {sorted(pd.Series(predictions).unique().tolist())}")
    
    return results_df

