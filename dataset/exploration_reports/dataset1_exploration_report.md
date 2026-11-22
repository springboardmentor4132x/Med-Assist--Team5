# Exploratory Data Analysis Report: Dataset 1
## Patient Profile and Disease Symptoms Datasets
**Files Analyzed:**
- Primary Raw Dataset: `dataset/Disease_symptom_and_patient_profile_dataset.csv`
- Existing Cleaned Dataset: `dataset/cleaned_disease_dataset.csv`

---

## 1. Executive Summary

Dataset 1 represents observational patient clinical profiles combining demographic indicators, vital health metrics, common symptoms, and diagnosed medical outcomes. This dataset directly aligns with the MedAssist AI platform architecture (`backend/services/predict.py`, database models, and the frontend user assessment workflow).

### Key Verified Metrics
| Metric | Raw Dataset (`Disease_symptom_and_patient_profile_dataset.csv`) | Cleaned Dataset (`cleaned_disease_dataset.csv`) | Difference / Note |
| :--- | :---: | :---: | :--- |
| **Total Rows** | 349 | 300 | 49 exact duplicate rows removed |
| **Total Columns** | 10 | 10 | Identical column definitions |
| **Missing / Null Values** | 0 (0.0%) | 0 (0.0%) | Complete data across all features |
| **Exact Duplicate Rows** | 49 (14.04%) | 0 (0.0%) | Fully deduplicated in cleaned file |
| **Unique Diseases** | 116 | 116 | All unique conditions preserved |
| **Unique Feature Profiles** | 244 | 244 | Distinct symptom/demographic combinations |
| **Outcome Balance** | 186 Pos / 163 Neg | 157 Pos / 143 Neg | 52.33% Positive / 47.67% Negative |
| **File Encoding** | UTF-8 | UTF-8 | Clean standard encoding |

---

## 2. Dataset Schema & Data Types

The dataset contains 10 columns comprising demographic metrics, physiological indicators, four binary clinical symptoms, disease label, and outcome status:

| Column Name | Python Data Type | Clinical Domain | Expected Values | Description |
| :--- | :---: | :--- | :--- | :--- |
| `Disease` | `object` (string) | Target / Diagnosis | 116 unique diseases | Diagnosed medical condition |
| `Fever` | `object` (string) | Binary Symptom | `Yes`, `No` | Elevated body temperature |
| `Cough` | `object` (string) | Binary Symptom | `Yes`, `No` | Persistent respiratory cough |
| `Fatigue` | `object` (string) | Binary Symptom | `Yes`, `No` | Generalized physical exhaustion |
| `Difficulty Breathing`| `object` (string) | Binary Symptom | `Yes`, `No` | Dyspnea / shortness of breath |
| `Age` | `int64` | Demographic | 19 – 90 years | Patient age in full years |
| `Gender` | `object` (string) | Demographic | `Female`, `Male` | Patient biological sex |
| `Blood Pressure` | `object` (string) | Clinical Vital | `Low`, `Normal`, `High` | Systemic arterial pressure tier |
| `Cholesterol Level` | `object` (string) | Laboratory Metric | `Low`, `Normal`, `High` | Serum cholesterol status tier |
| `Outcome Variable` | `object` (string) | Target / Outcome | `Positive`, `Negative` | Final clinical assessment flag |

---

## 3. First 10 Rows (Verified Data)

### 3.1 Raw Dataset (`Disease_symptom_and_patient_profile_dataset.csv`)
| Disease | Fever | Cough | Fatigue | Difficulty Breathing | Age | Gender | Blood Pressure | Cholesterol Level | Outcome Variable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Influenza | Yes | No | Yes | Yes | 19 | Female | Low | Normal | Positive |
| Common Cold | No | Yes | Yes | No | 25 | Female | Normal | Normal | Negative |
| Eczema | No | Yes | Yes | No | 25 | Female | Normal | Normal | Negative |
| Asthma | Yes | Yes | No | Yes | 25 | Male | Normal | Normal | Positive |
| Asthma | Yes | Yes | No | Yes | 25 | Male | Normal | Normal | Positive |
| Eczema | Yes | No | No | No | 25 | Female | Normal | Normal | Positive |
| Influenza | Yes | Yes | Yes | Yes | 25 | Female | Normal | Normal | Positive |
| Influenza | Yes | Yes | Yes | Yes | 25 | Female | Normal | Normal | Positive |
| Hyperthyroidism | No | Yes | No | No | 28 | Female | Normal | Normal | Negative |
| Hyperthyroidism | No | Yes | No | No | 28 | Female | Normal | Normal | Negative |

*Observations in Raw Dataset:*
- Row 4 is an exact duplicate of Row 3 (`Asthma`).
- Row 7 is an exact duplicate of Row 6 (`Influenza`).
- Row 9 is an exact duplicate of Row 8 (`Hyperthyroidism`).

### 3.2 Cleaned Dataset (`cleaned_disease_dataset.csv`)
| Disease | Fever | Cough | Fatigue | Difficulty Breathing | Age | Gender | Blood Pressure | Cholesterol Level | Outcome Variable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Influenza | Yes | No | Yes | Yes | 19 | Female | Low | Normal | Positive |
| Common Cold | No | Yes | Yes | No | 25 | Female | Normal | Normal | Negative |
| Eczema | No | Yes | Yes | No | 25 | Female | Normal | Normal | Negative |
| Asthma | Yes | Yes | No | Yes | 25 | Male | Normal | Normal | Positive |
| Eczema | Yes | No | No | No | 25 | Female | Normal | Normal | Positive |
| Influenza | Yes | Yes | Yes | Yes | 25 | Female | Normal | Normal | Positive |
| Hyperthyroidism | No | Yes | No | No | 28 | Female | Normal | Normal | Negative |
| Asthma | Yes | No | No | Yes | 28 | Male | High | Normal | Positive |
| Allergic Rhinitis | No | Yes | Yes | No | 29 | Female | Normal | Low | Negative |
| Anxiety Disorders | No | Yes | No | No | 29 | Female | Normal | High | Negative |

---

## 4. Verification of Equivalence

Programmatic comparison between `cleaned_disease_dataset.csv` and `df_raw.drop_duplicates()` confirms:
$$\text{df\_raw.drop\_duplicates().reset\_index(drop=True)} \equiv \text{df\_clean}$$
- **Assertion Result**: `True` (Bit-for-bit identical).
- **Conclusion**: `cleaned_disease_dataset.csv` is solely the deduplicated version of `Disease_symptom_and_patient_profile_dataset.csv`. It contains **no** column renames, **no** binary one-hot encoding, and **no** label transformations.

---

## 5. Duplicate Rows Investigation

- **Total Rows Involved in Duplication**: 98 rows (49 initial records + 49 redundant replicas).
- **Redundancy Analysis**: Across all 10 columns simultaneously (including `Disease`, `Age`, `Gender`, and `Outcome Variable`), the 49 rows are verbatim clones.
- **Top Duplicated Diseases in Raw File**:
  - Asthma (duplicated 3 times)
  - Diabetes (duplicated 2 times)
  - Influenza (duplicated 2 times)
  - Stroke (duplicated 2 times)
  - Osteoporosis (duplicated 2 times)
- **Clinical Recommendation**: Removing these 49 exact duplicate rows is strictly justified to prevent data leakage during train/test splits and to eliminate artificial weight inflation during model training.

---

## 6. Numerical Feature Analysis (`Age`)

| Statistic | Raw Dataset (349 rows) | Cleaned Dataset (300 rows) |
| :--- | :---: | :---: |
| **Count** | 349 | 300 |
| **Mean** | 46.32 years | 45.76 years |
| **Standard Deviation** | 13.09 years | 12.60 years |
| **Minimum** | 19.00 years | 19.00 years |
| **25th Percentile (Q1)** | 35.00 years | 35.00 years |
| **50th Percentile (Median)**| 45.00 years | 45.00 years |
| **75th Percentile (Q3)** | 55.00 years | 55.00 years |
| **Maximum** | 90.00 years | 90.00 years |
| **Interquartile Range (IQR)** | 20.00 years | 20.00 years |

*Distribution Notes:*
- Minimum age is 19 (adult population only; pediatric cases <19 are absent).
- Maximum age is 90.
- Outlier test: $Q1 - 1.5 \times \text{IQR} = 35 - 30 = 5$; $Q3 + 1.5 \times \text{IQR} = 55 + 30 = 85$. Exactly two patients are aged 90, which is clinically valid for geriatric diseases (e.g., Osteoporosis, Alzheimer's). No data entry errors detected.

---

## 7. Categorical & Clinical Distributions

### 7.1 Symptoms (Deduplicated vs Raw)
| Symptom Column | Raw Counts (`Yes` / `No`) | Cleaned Counts (`Yes` / `No`) | Cleaned Percent `Yes` |
| :--- | :---: | :---: | :---: |
| **Fever** | 175 / 174 | 143 / 157 | 47.67% |
| **Cough** | 167 / 182 | 140 / 160 | 46.67% |
| **Fatigue** | 242 / 107 | 212 / 88 | 70.67% |
| **Difficulty Breathing** | 88 / 261 | 73 / 227 | 24.33% |

*Clinical Insight:*
- `Fatigue` is the most prevalent symptom (reported in 70.67% of cases).
- `Difficulty Breathing` is the least prevalent (reported in only 24.33% of cases), making it a high-specificity indicator for cardiopulmonary conditions.

### 7.2 Demographic & Physiological Features
| Feature | Cleaned Categories | Count | Percentage |
| :--- | :--- | :---: | :---: |
| **Gender** | Female | 152 | 50.67% |
| | Male | 148 | 49.33% |
| **Blood Pressure** | High | 143 | 47.67% |
| | Normal | 139 | 46.33% |
| | Low | 18 | 6.00% |
| **Cholesterol Level** | High | 140 | 46.67% |
| | Normal | 130 | 43.33% |
| | Low | 30 | 10.00% |

*Clinical Insight:*
- Gender representation is exceptionally well balanced (50.7% Female vs 49.3% Male).
- `Low` categories in both Blood Pressure (6%) and Cholesterol (10%) are relatively sparse compared to `Normal` and `High`.

### 7.3 Target Variables
- **Outcome Variable**:
  - `Positive`: 157 (52.33%)
  - `Negative`: 143 (47.67%)
  - Balanced binary target distribution; no severe class imbalance mitigation (e.g., SMOTE) is mandatory.
- **Disease Column**:
  - Total Unique Conditions: **116**
  - Most Frequent Diseases:
    1. Asthma: 20 records
    2. Stroke: 14 records
    3. Osteoporosis: 12 records
    4. Hypertension: 9 records
    5. Diabetes: 8 records
    6. Migraine: 8 records
    7. Influenza: 6 records
    8. Pneumonia: 6 records
    9. Bronchitis: 6 records
    10. Hyperthyroidism: 6 records
  - Diseases with exactly 1 record: **61 conditions** (52.6% of all diseases).
  - *Critical Warning for Model Training*: Training a multiclass classifier directly on `Disease` with 116 classes across only 300 samples is statistically underdetermined due to high label sparsity (61 singleton classes). However, binary classification on `Outcome Variable` is well-conditioned.

---

## 8. In-Depth Clinical Investigation: Feature Overlaps & Conflicts

A rigorous feature profile analysis was conducted over the 8 feature columns:
$$\vec{x} = [\text{Fever, Cough, Fatigue, Difficulty Breathing, Age, Gender, Blood Pressure, Cholesterol Level}]$$

### 8.1 Investigation: 45 Profiles with Multiple Disease Labels
- **Finding**: In the deduplicated dataset, there are **244 distinct feature profiles**.
- **Result**: Exactly **45 feature groups** map to more than one disease label.
- **Clinical Explanation**: This is expected medical reality. Common clinical presentations (e.g., a 35-year-old male with Fever, Cough, Fatigue, High BP, and High Cholesterol) can naturally present in both Bronchitis and Pneumonia. The 4 symptom features do not constitute an exhaustive differential diagnostic panel.

### 8.2 Investigation: 7 Profiles with Conflicting Outcome Variables
- **Finding**: Exactly **7 feature groups** (comprising 16 rows) share the exact same 8 input features but have opposing `Outcome Variable` values (`Positive` vs `Negative`).
- **Complete Inventory of Conflicting Records**:

| Group | Age | Gender | Fever | Cough | Fatigue | Diff. Breathing | BP | Cholesterol | Diagnosed Disease | Outcome |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | 35 | Female | No | No | Yes | No | Normal | Low | Allergic Rhinitis | **Negative** |
| | 35 | Female | No | No | Yes | No | Normal | Low | Rheumatoid Arthritis | **Positive** |
| **2** | 35 | Male | No | No | Yes | No | High | High | Epilepsy | **Negative** |
| | 35 | Male | No | No | Yes | No | High | High | Kidney Cancer | **Positive** |
| | 35 | Male | No | No | Yes | No | High | High | Liver Disease | **Positive** |
| | 35 | Male | No | No | Yes | No | High | High | Ulcerative Colitis | **Positive** |
| **3** | 65 | Male | No | No | Yes | No | Normal | High | Diabetes | **Negative** |
| | 65 | Male | No | No | Yes | No | Normal | High | Mumps | **Positive** |
| **4** | 40 | Male | No | No | Yes | Yes | High | High | Cystic Fibrosis | **Negative** |
| | 40 | Male | No | No | Yes | Yes | High | High | Asthma | **Positive** |
| **5** | 35 | Male | No | Yes | Yes | No | High | High | Urinary Tract Infection | **Negative** |
| | 35 | Male | No | Yes | Yes | No | High | High | Migraine | **Positive** |
| **6** | 30 | Female | Yes | No | No | No | Normal | Normal | Migraine | **Negative** |
| | 30 | Female | Yes | No | No | No | Normal | Normal | Urinary Tract Infection | **Positive** |
| **7** | 45 | Female | Yes | No | Yes | No | High | High | Hepatitis | **Negative** |
| | 45 | Female | Yes | No | Yes | No | High | High | Diabetes | **Positive** |

### 8.3 Machine Learning Impact of Conflicting Profiles
1. **Bayes Error Bound**: Any deterministic or probabilistic machine learning model trained solely on these 8 features cannot achieve 100% training accuracy because identical inputs map to divergent target labels (an irreducible error of at least $7 / 300 = 2.33\%$).
2. **Clinical Reason**: The outcome status depends on pathology specific to the underlying disease (e.g., active systemic inflammation in Rheumatoid Arthritis vs localized histamine response in Allergic Rhinitis), which cannot be captured by the 4 recorded symptoms alone.
3. **Recommendation**: Teammates training classifiers must be aware of this irreducible noise floor and should not force 100% training accuracy to avoid catastrophic overfitting.

---

## 9. Data Quality & Preprocessing Recommendations

1. **Missing Data**: No imputation required (0 missing cells).
2. **Deduplication**: Drop the 49 redundant rows to retain the 300 unique cases.
3. **Symptom Normalization**: Convert `'Yes'/'No'` in `Fever`, `Cough`, `Fatigue`, `Difficulty Breathing` to integer binary flags `1/0`.
4. **Target Encoding**: Convert `Outcome Variable` `'Positive'/'Negative'` to integer flags `1/0`.
5. **Column Standardization**: Convert column headers to `lower_snake_case` (e.g., `difficulty_breathing`, `blood_pressure`).
6. **Preservation**: Retain the original file `Disease_symptom_and_patient_profile_dataset.csv` untouched. Save transformed outputs strictly to `dataset/processed/`.
