import joblib
import pandas as pd
from pathlib import Path
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
data = pd.read_csv(BASE.parent / "data" / "penguins.csv").dropna()

le = preprocessing.LabelEncoder()
X = data[["bill_length_mm", "flipper_length_mm"]]
y = le.fit_transform(data["species"])

clf = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=11)),
])
clf.fit(X, y)

(BASE / "artifacts").mkdir(exist_ok=True)
joblib.dump(clf, BASE / "artifacts" / "pipeline.joblib")
joblib.dump(le, BASE / "artifacts" / "label_encoder.joblib")
