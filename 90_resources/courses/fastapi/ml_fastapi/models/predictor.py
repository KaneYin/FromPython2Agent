import joblib
from pathlib import Path

_BASE = Path(__file__).resolve().parent
_clf = joblib.load(_BASE / "artifacts" / "pipeline.joblib")
_le = joblib.load(_BASE / "artifacts" / "label_encoder.joblib")

def predict_species(bill_length_mm: float, flipper_length_mm: float) -> str:
    pred = _clf.predict([[bill_length_mm, flipper_length_mm]])
    return _le.inverse_transform(pred)[0]
