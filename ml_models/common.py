"""
MedAssist AI - Module 3: shared helpers for model training and evaluation.

Used by:
    ml_models/training/train_models.py       (Member 2 - model training)
    ml_models/evaluation/evaluate_models.py  (Member 3 - evaluation & selection)

Everything that must stay identical between training and evaluation lives
here (feature columns, train/test split, model definitions), so the two
scripts never drift apart.
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

# SVC(probability=True) is flagged as deprecated in the newest scikit-learn,
# but it still works and is the simplest way to get probability scores.
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

# ---------------------------------------------------------------- paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "dataset" / "processed" / "cleaned_disease_dataset.csv"
ML_DIR = PROJECT_ROOT / "ml_models"
TRAINED_DIR = ML_DIR / "trained_models"
REPORTS_DIR = ML_DIR / "reports"

# ------------------------------------------------------------- settings
RANDOM_STATE = 42
TEST_SIZE = 0.20
MIN_CLASS_FOR_CV = 5  # diseases with fewer samples cannot be cross-validated

SYMPTOM_COLS = ["fever", "cough", "fatigue", "difficulty_breathing"]
CATEGORICAL_COLS = ["gender", "blood_pressure", "cholesterol_level"]
NUMERIC_COLS = ["age"]
FEATURE_COLS = SYMPTOM_COLS + NUMERIC_COLS + CATEGORICAL_COLS

# Two prediction tasks. "disease" is what the module brief asks for
# (disease categories + top 3). "outcome" is the well-conditioned binary
# target Prabhas recommended in TEAM_HANDOFF.md.
TASKS = {
    "disease": "disease",
    "outcome": "outcome_binary",
}

MODEL_NAMES = [
    "decision_tree",
    "random_forest",
    "svm",
    "xgboost",
    "logistic_regression",
]

MODEL_LABELS = {
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
    "svm": "SVM (RBF)",
    "xgboost": "XGBoost",
    "logistic_regression": "Logistic Regression",
}


# ----------------------------------------------------------------- data
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"{DATA_FILE} not found. Run dataset/preprocessing/preprocess_dataset.py first."
        )
    return pd.read_csv(DATA_FILE)


def encode_target(df: pd.DataFrame, task: str):
    """Return (y_encoded, label_encoder) for a task.

    The disease names are turned into integers 0..N-1 with a LabelEncoder
    fitted on ALL diseases, so every model (including XGBoost, which needs
    integer labels) uses the same ids. The encoder is saved next to the
    models so predictions can be turned back into disease names.
    """
    column = TASKS[task]
    if task == "outcome":
        encoder = LabelEncoder().fit([0, 1])
        return df[column].to_numpy(), encoder
    encoder = LabelEncoder().fit(df[column])
    return encoder.transform(df[column]), encoder


def make_split(df: pd.DataFrame, y: np.ndarray, task: str):
    """Train/test split (80/20, seed 42). Returns index arrays.

    outcome: normal stratified split.
    disease: many diseases appear only once, and a stratified split cannot
    put a single sample in both sets. So diseases that appear only once
    always go to the training set (the model still learns them), and the
    rest are split with stratification.
    """
    idx = np.arange(len(df))
    if task == "outcome":
        return train_test_split(
            idx, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )

    counts = pd.Series(y).value_counts()
    singleton = pd.Series(y).map(counts).to_numpy() < 2
    forced_train = idx[singleton]
    rest = idx[~singleton]
    tr, te = train_test_split(
        rest, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y[rest]
    )
    return np.concatenate([forced_train, tr]), te


def cv_subset(df: pd.DataFrame, y: np.ndarray, task: str, encoder):
    """Rows that can be used for stratified cross-validation.

    outcome: every row. disease: only diseases with >= MIN_CLASS_FOR_CV rows,
    with labels re-numbered 0..k-1 (needed by XGBoost).
    Returns (rows, labels, class_names) where class_names[i] is the name of
    label i.
    """
    if task == "outcome":
        return df, y, np.array(["Negative", "Positive"])
    counts = pd.Series(y).value_counts()
    keep = pd.Series(y).map(counts).to_numpy() >= MIN_CLASS_FOR_CV
    original_ids = np.unique(y[keep])  # sorted, same order LabelEncoder uses
    sub_y = LabelEncoder().fit_transform(y[keep])
    return (
        df[keep].reset_index(drop=True),
        sub_y,
        encoder.classes_[original_ids],
    )


# ---------------------------------------------------------------- models
def make_preprocessor(scale_age: bool) -> ColumnTransformer:
    """Same preprocessing is used in training and in prediction because it
    lives inside the saved pipeline: raw patient columns in, features out."""
    return ColumnTransformer(
        [
            ("symptoms", "passthrough", SYMPTOM_COLS),
            ("age", StandardScaler() if scale_age else "passthrough", NUMERIC_COLS),
            (
                "categories",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLS,
            ),
        ]
    )


def build_model(name: str, task: str) -> Pipeline:
    """Create an untrained pipeline (preprocessing + classifier)."""
    binary = task == "outcome"

    if name == "decision_tree":
        clf = DecisionTreeClassifier(
            max_depth=6 if binary else 12,
            min_samples_leaf=3 if binary else 1,
            random_state=RANDOM_STATE,
        )
        scale = False
    elif name == "random_forest":
        # disease task has 116 classes, so full-depth trees make a huge
        # file (80 MB). Limiting depth/leaf size keeps it small and also
        # reduces overfitting on 300 rows.
        clf = RandomForestClassifier(
            n_estimators=300 if binary else 100,
            max_depth=None if binary else 8,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        scale = False
    elif name == "svm":
        clf = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            probability=True,  # needed for probability scores / top 3
            random_state=RANDOM_STATE,
        )
        scale = True
    elif name == "xgboost":
        clf = XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            subsample=0.9,
            random_state=RANDOM_STATE,
            n_jobs=1,
            verbosity=0,
        )
        scale = False
    elif name == "logistic_regression":
        clf = LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)
        scale = True
    else:
        raise ValueError(f"Unknown model: {name}")

    return Pipeline([("prep", make_preprocessor(scale)), ("clf", clf)])


def top_k_accuracy(proba: np.ndarray, classes: np.ndarray, y_true: np.ndarray, k=3):
    """Share of rows whose true label is inside the k highest-scored classes."""
    k = min(k, proba.shape[1])
    top = np.argsort(proba, axis=1)[:, -k:]
    top_labels = classes[top]
    return float(np.mean([t in row for t, row in zip(y_true, top_labels)]))


def predict_labels(model, X) -> np.ndarray:
    """Predicted label = class with the highest probability score.

    Used everywhere instead of model.predict(), because the app shows the
    probability ranking. (SVC.predict can disagree with its own
    predict_proba on a few rows.)
    """
    return model.classes_[model.predict_proba(X).argmax(axis=1)]
