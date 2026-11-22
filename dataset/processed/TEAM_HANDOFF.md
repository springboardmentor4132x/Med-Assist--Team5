# Team Handoff Documentation: Processed Disease Dataset
## MedAssist AI – Data Engineering Handoff to Modeling Team
**Dataset Release Version:** 1.0.0 (Cleaned & Standardized)  
**Date:** 2026-11-22  
**Handoff By:** Prabhas Pondara (Module 3 Lead: Dataset Exploration & Preprocessing)

---

## 1. Quick Reference & File Locations

| Asset | Path | Description |
| :--- | :--- | :--- |
| **Processed Dataset** | [`dataset/processed/cleaned_disease_dataset.csv`](file:///c:/INFOSYS/Med-Assist--Team5/dataset/processed/cleaned_disease_dataset.csv) | Clean, deduplicated, standardized dataset ready for modeling |
| **Raw Original Dataset** | [`dataset/Disease_symptom_and_patient_profile_dataset.csv`](file:///c:/INFOSYS/Med-Assist--Team5/dataset/Disease_symptom_and_patient_profile_dataset.csv) | Untouched original Kaggle dataset (kept for reference) |
| **Preprocessing Script** | [`dataset/preprocessing/preprocess_dataset.py`](file:///c:/INFOSYS/Med-Assist--Team5/dataset/preprocessing/preprocess_dataset.py) | Fully automated, reproducible preprocessing script |
| **Audit Summary** | [`dataset/processed/preprocessing_summary.md`](file:///c:/INFOSYS/Med-Assist--Team5/dataset/processed/preprocessing_summary.md) | Technical audit log of transformations |
| **EDA Reports** | [`dataset/exploration_reports/`](file:///c:/INFOSYS/Med-Assist--Team5/dataset/exploration_reports/) | Complete Phase 1 EDA documentation |

---

## 2. Dataset Schema & Column Specification

The cleaned dataset contains **300 rows × 11 columns**:

| Column Name | Type | Value Range / Categories | Role in ML Modeling | Encoding Note |
| :--- | :---: | :--- | :--- | :--- |
| `disease` | `string` | 116 unique diseases | Secondary Target / Multiclass Label | Readable text condition name |
| `fever` | `int64` | `0`, `1` | Binary Input Feature | $0 = \text{No}, 1 = \text{Yes}$ |
| `cough` | `int64` | `0`, `1` | Binary Input Feature | $0 = \text{No}, 1 = \text{Yes}$ |
| `fatigue` | `int64` | `0`, `1` | Binary Input Feature | $0 = \text{No}, 1 = \text{Yes}$ |
| `difficulty_breathing`| `int64` | `0`, `1` | Binary Input Feature | $0 = \text{No}, 1 = \text{Yes}$ |
| `age` | `int64` | $19 - 90$ | Continuous Numeric Feature | Standard integer patient age |
| `gender` | `string` | `'Female'`, `'Male'` | Categorical Feature | Requires one-hot encoding for ML |
| `blood_pressure` | `string` | `'Low'`, `'Normal'`, `'High'` | Ordinal / Categorical Feature | Can be one-hot or ordinally encoded |
| `cholesterol_level` | `string` | `'Low'`, `'Normal'`, `'High'` | Ordinal / Categorical Feature | Can be one-hot or ordinally encoded |
| `outcome_variable` | `string` | `'Positive'`, `'Negative'` | Primary Human-Readable Target | Clean string for logs & UI |
| `outcome_binary` | `int64` | `0`, `1` | **Primary Machine Learning Target** | $0 = \text{Negative}, 1 = \text{Positive}$ |

---

## 3. Transformations Summary (Before vs After)

- **Rows**: Reduced from 349 to **300** by eliminating 49 exact duplicate rows.
- **Columns**: Increased from 10 to **11** by standardizing column names and adding `outcome_binary`.
- **Missing Values**: 0 missing values (100% complete).
- **Duplicate Records**: Exactly 0 duplicates remain.
- **Symptom Flags**: Transformed from string `'Yes'/'No'` to integer `1/0`.

---

## 4. How to Load and Use in Python (Pandas & Scikit-Learn)

### 4.1 Loading the Cleaned Data
```python
import pandas as pd

# Load the processed dataset using a relative path
df = pd.read_csv("dataset/processed/cleaned_disease_dataset.csv")

print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns successfully.")
print(df.head(3))
```

### 4.2 Preparing Features and Target for Binary Classification (`Outcome Variable`)
```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataset/processed/cleaned_disease_dataset.csv")

# Feature columns (matching backend/services/predict.py)
feature_cols = [
    "fever",
    "cough",
    "fatigue",
    "difficulty_breathing",
    "age",
    "gender",
    "blood_pressure",
    "cholesterol_level",
]

X = df[feature_cols]
y = df["outcome_binary"]  # 1 = Positive, 0 = Negative

# One-hot encode categorical features (gender, blood_pressure, cholesterol_level)
X_encoded = pd.get_dummies(X, columns=["gender", "blood_pressure", "cholesterol_level"], dtype=int)

# Stratified train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
```

---

## 5. Critical Clinical & Machine Learning Warnings for Teammates

### 5.1 Conflicting Outcomes (Irreducible Error Floor)
- **Investigation Finding**: There are **7 feature profiles (spanning 16 patient records)** that share identical feature values across all 8 inputs but have opposing target values (`Positive` in some, `Negative` in others).
- **Reason**: The outcome is determined by the specific underlying pathology (e.g., active disease in a patient with Rheumatoid Arthritis vs localized mild symptoms in Allergic Rhinitis) which the 4 symptoms alone cannot differentiate.
- **Modeling Directive**: Do **not** attempt to force 100% training accuracy. An irreducible Bayes error floor of $\approx 2.33\%$ exists. Overfitting to resolve these conflicts will impair generalization on test data.

### 5.2 Multiclass Disease Classification Warning
- If teammates intend to predict `disease` (multiclass classification):
  - Note that there are **116 distinct disease classes** across only **300 total samples**.
  - **61 diseases have only a single sample ($N=1$)**, making standard cross-validation mathematically impossible without class filtering or grouping.
  - Predicting binary `outcome_binary` is well-conditioned (157 Positive vs 143 Negative).

### 5.3 Datasets Kept Separate
- `dataset/trainings.csv` and `dataset/testing.csv` contain 1,326 binary symptoms and 0 demographic fields. They have completely incompatible schemas and **must not be merged** with this patient profile dataset.
