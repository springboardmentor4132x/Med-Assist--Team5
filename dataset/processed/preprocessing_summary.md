# Data Preprocessing Summary Report
## MedAssist AI – Module 3: Preprocessing Pipeline
**Module Status:** Preprocessing Pipeline Completed  
**Generated Date:** 2026-11-22  
**Input Dataset:** `dataset/Disease_symptom_and_patient_profile_dataset.csv`  
**Cleaned Output:** `dataset/processed/cleaned_disease_dataset.csv`  
**Execution Script:** `dataset/preprocessing/preprocess_dataset.py`  
**Lead Engineer:** Prabhas Pondara (MedAssist AI Team 5)

---

## 1. Executive Preprocessing Audit

The preprocessing pipeline implements the recommendations from the Phase 1 Exploratory Data Analysis. It cleans, standardizes, and encodes the patient profile dataset while preserving original medical observations and protecting against artificial data leakage.

### Summary of Dataset Evolution

| Metric / Dimension | Raw Dataset (Before) | Cleaned Dataset (After) | Change / Operational Justification |
| :--- | :---: | :---: | :--- |
| **File Location** | `dataset/` | `dataset/processed/` | Original preserved untouched; clean file isolated |
| **Row Count** | 349 | 300 | 49 exact duplicate rows removed |
| **Column Count** | 10 | 11 | Snake_cased + additional `outcome_binary` target column |
| **Missing Values** | 0 (0.0%) | 0 (0.0%) | 100% complete data maintained |
| **Duplicate Rows** | 49 (14.04%) | 0 (0.0%) | Exact duplicates eliminated |
| **Symptom Representation** | String (`Yes` / `No`) | Integer (`1` / `0`) | Binary encoding for ML compatibility |
| **Outcome Representation** | String (`Positive`/`Negative`)| String + Integer (`1`/`0`)| Preserved human label + added binary model target |
| **Column Casing** | Title Case with Spaces | Lowercase `snake_case` | Standard programming conventions |
| **Conflicting Profiles** | 7 profiles (16 rows) | 7 profiles (16 rows) | **Strictly preserved** (valid clinical nuance) |
| **Unique Diseases** | 116 | 116 | All unique conditions preserved |

---

## 2. Transformations Applied

### 2.1 Non-Destructive Ingestion
- The raw dataset `dataset/Disease_symptom_and_patient_profile_dataset.csv` is loaded using Pandas without in-place modification.
- The original file on disk remains completely unchanged.

### 2.2 Deduplication
- **Operation**: `df.drop_duplicates().reset_index(drop=True)`
- **Impact**: Exactly 49 redundant duplicate rows removed (reducing rows from 349 to 300).
- **Justification**: The 49 rows are exact, identical clones across all 10 features and targets. Removing them eliminates artificial sample inflation and prevents training/testing cross-contamination during cross-validation.

### 2.3 Column Name Standardization
All column headers were converted to lowercase `snake_case`:
- `Disease` $\rightarrow$ `disease`
- `Fever` $\rightarrow$ `fever`
- `Cough` $\rightarrow$ `cough`
- `Fatigue` $\rightarrow$ `fatigue`
- `Difficulty Breathing` $\rightarrow$ `difficulty_breathing`
- `Age` $\rightarrow$ `age`
- `Gender` $\rightarrow$ `gender`
- `Blood Pressure` $\rightarrow$ `blood_pressure`
- `Cholesterol Level` $\rightarrow$ `cholesterol_level`
- `Outcome Variable` $\rightarrow$ `outcome_variable`
- `outcome_binary` (newly added column)

### 2.4 Symptom Feature Binary Encoding
Symptom columns (`fever`, `cough`, `fatigue`, `difficulty_breathing`) were converted from string flags to integer indicators:
- `'Yes'` $\rightarrow 1$
- `'No'` $\rightarrow 0$
- Data type: `int64`

### 2.5 Categorical Text Normalization
- All string columns (`disease`, `gender`, `blood_pressure`, `cholesterol_level`, `outcome_variable`) were stripped of leading and trailing whitespace.
- Standard capitalization applied:
  - `gender`: `'Female'`, `'Male'`
  - `blood_pressure`: `'Low'`, `'Normal'`, `'High'`
  - `cholesterol_level`: `'Low'`, `'Normal'`, `'High'`
  - `outcome_variable`: `'Positive'`, `'Negative'`

### 2.6 Dual Target Representation
To support teammates building machine learning models without sacrificing human interpretability:
1. `outcome_variable`: Preserved as clean text (`'Positive'`, `'Negative'`).
2. `outcome_binary`: Mapped to binary integer (`1` for Positive, `0` for Negative) typed as `int64`.

### 2.7 Preservation of Conflicting Feature Profiles
- In compliance with clinical domain requirements, the 7 feature profiles that share identical inputs but have divergent outcomes were **not** deleted or modified.
- Removing clinical conflicts would distort the true Bayes error rate of clinical triage based on broad symptoms.

---

## 3. Post-Processing Verification & Quality Audit

The processed dataset was verified against strict quality assertions:

```text
[VALIDATION PASSED] Clean Rows: 300
[VALIDATION PASSED] Clean Columns: 11
[VALIDATION PASSED] Null Count: 0
[VALIDATION PASSED] Duplicate Count: 0
[VALIDATION PASSED] Conflicting Profiles Preserved: 7
```

### 3.1 Feature Distributions (Cleaned Data)

| Feature | Data Type | Categories / Values | Counts / Statistics |
| :--- | :---: | :--- | :--- |
| `disease` | `string` | 116 unique diseases | Most frequent: Asthma (20), Stroke (14), Osteoporosis (12) |
| `fever` | `int64` | `0` (No), `1` (Yes) | `0`: 157 (52.33%) \| `1`: 143 (47.67%) |
| `cough` | `int64` | `0` (No), `1` (Yes) | `0`: 160 (53.33%) \| `1`: 140 (46.67%) |
| `fatigue` | `int64` | `0` (No), `1` (Yes) | `0`: 88 (29.33%) \| `1`: 212 (70.67%) |
| `difficulty_breathing`| `int64` | `0` (No), `1` (Yes) | `0`: 227 (75.67%) \| `1`: 73 (24.33%) |
| `age` | `int64` | Min: 19, Max: 90 | Mean: 45.76, Std: 12.60, Median: 45.0 |
| `gender` | `string` | `'Female'`, `'Male'` | Female: 152 (50.67%) \| Male: 148 (49.33%) |
| `blood_pressure` | `string` | `'High'`, `'Normal'`, `'Low'` | High: 143 (47.67%) \| Normal: 139 (46.33%) \| Low: 18 (6.00%) |
| `cholesterol_level` | `string` | `'High'`, `'Normal'`, `'Low'` | High: 140 (46.67%) \| Normal: 130 (43.33%) \| Low: 30 (10.00%) |
| `outcome_variable` | `string` | `'Positive'`, `'Negative'` | Positive: 157 (52.33%) \| Negative: 143 (47.67%) |
| `outcome_binary` | `int64` | `1` (Positive), `0` (Negative)| `1`: 157 (52.33%) \| `0`: 143 (47.67%) |

---

## 4. Reusable Script Usage

Teammates can re-run or inspect the preprocessing pipeline at any time:

```bash
# Run with project defaults
python dataset/preprocessing/preprocess_dataset.py

# Or specify custom paths if needed
python dataset/preprocessing/preprocess_dataset.py --input-file dataset/Disease_symptom_and_patient_profile_dataset.csv --output-dir dataset/processed --output-file cleaned_disease_dataset.csv
```
