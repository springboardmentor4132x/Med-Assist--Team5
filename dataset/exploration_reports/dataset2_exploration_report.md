# Exploratory Data Analysis Report: Dataset 2
## Granular Binary Symptom & Disease Prognosis Datasets
**Files Analyzed:**
- Primary Training Dataset: `dataset/trainings.csv`
- Primary Testing Dataset: `dataset/testing.csv`

---

## 1. Executive Summary

Dataset 2 consists of high-dimensional, binary symptom incidence matrices paired with disease prognoses (`Prognosis`). Unlike Dataset 1, which represents clinical observation of individual patients (with vitals and demographic data), Dataset 2 functions as a diagnostic medical ontology or lookup table detailing which of 1,326 granular symptoms are associated with specific diseases.

### Key Verified Metrics
| Metric | Training Dataset (`trainings.csv`) | Testing Dataset (`testing.csv`) | Notes & Characteristics |
| :--- | :---: | :---: | :--- |
| **Row Count** | 391 | 414 | 391 diseases in train; 414 cases in test |
| **Column Count** | 1,327 | 1,327 | 1,326 symptoms + 1 target (`Prognosis`) |
| **Feature Data Types** | `int64` (1,326 columns) | `int64` (1,326 columns) | Strictly binary values $\{0, 1\}$ |
| **Target Data Type** | `object` (string) | `object` (string) | Disease diagnosis name |
| **Missing Values** | 0 (0.0%) | 0 (0.0%) | Fully populated across all cells |
| **Exact Duplicate Rows** | 0 (0.0%) | 0 (0.0%) | Zero duplicate rows |
| **Unique Diseases** | 391 (1 per row) | 389 | 389 overlap; 2 train-only; 25 duplicate targets in test |
| **Mean Active Symptoms** | 7.81 symptoms/row | 9.23 symptoms/row | Matrix sparsity $> 99.4\%$ |
| **File Encoding** | Latin-1 / CP1252 | Latin-1 / CP1252 | Contains byte `0xa0` (non-breaking space) |

---

## 2. Dataset Schema & Structure

### 2.1 Feature Space (1,326 Binary Symptom Columns)
- All 1,326 feature columns are strictly typed as `int64`.
- Every value is strictly binary: $x_{ij} \in \{0, 1\}$.
- Feature names describe highly specialized anatomical, physical, and sensory manifestations (e.g., `'Downward palpebral slant to eyes'`, `'Mildly sunken chest (pectus excavatum)'`, `'Hairline with a "widow\'s peak"'`, `'Frequent styes(bumps)'`).
- There are **zero demographic or physiological features** in this dataset (no `Age`, `Gender`, `Blood Pressure`, or `Cholesterol Level`).

### 2.2 Target Variable (`Prognosis`)
- Name: `Prognosis`
- Type: `object` (string)
- Scope: Comprehensive medical diagnoses spanning genetic syndromes, acute poisonings, infectious diseases, and chronic disorders (e.g., *Aarskog syndrome, Achalasia, Acetone poisoning, Down syndrome, Malaria*).

---

## 3. Representative Data Slice (First 10 Rows)

Because displaying 1,327 columns is impractical, the table below provides a representative cross-section showing the first 6 symptom columns, 3 trailing symptom columns, and the target column `Prognosis`.

### 3.1 `trainings.csv` (First 10 Rows)
| Belly button that sticks out | Bulge in groin/scrotum | Delayed sexual maturity | Delayed teeth | Downward palpebral slant to eyes | Hairline with widow's peak | Slight blurring of vision | Frequent styes | Pressure in ear | Prognosis |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | Aarskog syndrome |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Aase syndrome |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Abdominal aortic aneurysm |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Abnormal uterine bleeding (AUB) |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Acetaminophen & codeine overdose |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Acetone poisoning |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Achalasia |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Achondrogenesis |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Achondroplasia |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Acid soldering flux poisoning |

---

## 4. Sparsity & Symptom Distribution

### 4.1 Matrix Sparsity Statistics
| Metric | Training Dataset (`trainings.csv`) | Testing Dataset (`testing.csv`) |
| :--- | :---: | :---: |
| **Total Symptom Cells** | $391 \times 1,326 = 518,466$ | $414 \times 1,326 = 548,964$ |
| **Active Symptom Cells (`1`)**| 3,054 (0.589%) | 3,822 (0.696%) |
| **Inactive Cells (`0`)** | 515,412 (99.411%) | 545,142 (99.304%) |
| **Mean Active Symptoms / Row**| **7.81** | **9.23** |
| **Standard Deviation** | 3.80 | 5.27 |
| **Minimum Active Symptoms** | 3 | 1 |
| **Median (50th Percentile)** | 7 | 8 |
| **Maximum Active Symptoms** | 36 | 39 |

*Clinical Insight:*
Across 1,326 possible symptoms, any individual disease presents with an average of only 7 to 9 active symptoms. This extreme sparsity reflects medical reality: specialized symptoms are highly disease-specific indicators.

---

## 5. Disease Target Analysis & Train/Test Overlap

### 5.1 Training Set Class Distribution
- `trainings.csv` contains exactly **391 unique diseases** across **391 rows**.
- **Every single disease has exactly 1 training example**.
- *Machine Learning Ramification*: Standard stratified K-Fold cross-validation cannot be performed on this training set, because no class has $k \ge 2$ samples.

### 5.2 Testing Set Class Distribution
- `testing.csv` contains **414 rows** representing **389 unique diseases**.
- **Class Overlap**: All 389 unique diseases in `testing.csv` exist in `trainings.csv`.
- **Train-Only Diseases**: Exactly 2 diseases appear in `trainings.csv` but are absent in `testing.csv`:
  1. *Aarskog syndrome*
  2. *Acid soldering flux poisoning*
- **Multiple Test Samples**: Exactly 25 diseases appear twice in `testing.csv` (with slightly varied symptom vectors), explaining the difference between 389 unique diseases and 414 total rows.

### 5.3 Overlap with Dataset 1 (`Disease_symptom_and_patient_profile_dataset.csv`)
- When comparing the 116 diseases in Dataset 1 with the 391 prognoses in `trainings.csv`:
  - **Shared Diseases**: Exactly **33 conditions** overlap (e.g., *Common Cold, Malaria, Measles, Allergic Rhinitis, Bipolar Disorder, Cirrhosis, Down Syndrome, Hemorrhoids*).
  - **Dataset 1 Specific**: 83 conditions are unique to Dataset 1.
  - **Dataset 2 Specific**: 358 conditions are unique to Dataset 2.

---

## 6. Data Quality & Encoding Anomalies

### 6.1 Non-Standard Character Encoding (Byte `0xa0`)
- **Issue**: Attempting to load `trainings.csv` or `testing.csv` using Python's default `utf-8` codec causes an immediate crash:
  ```text
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position 32: invalid start byte
  ```
- **Cause**: The raw files contain the non-breaking space character `\xa0` (Latin-1 / Windows-1252) within column headers and disease names.
  - Example Column: `'Downward palpebral slant to eyes\xa0'`
  - Example Disease: `'Abdominal aortic\xa0aneurysm'`
- **Mitigation for Teammates**: Load using `pd.read_csv('dataset/trainings.csv', encoding='latin1')` or `encoding='cp1252'`, and sanitize column headers with `.str.replace('\xa0', ' ').str.strip()`.

### 6.2 Zero Values / Missing Values
- There are **0 missing or null values** in either dataset.
- All 1,326 feature values are strictly binary integers $\{0, 1\}$.

---

## 7. Pipeline Incompatibility with Dataset 1

`trainings.csv` and `testing.csv` **cannot** be processed using the same pipeline as Dataset 1 (`Disease_symptom_and_patient_profile_dataset.csv`):

1. **Dimensional Mismatch**: 10 columns vs 1,327 columns.
2. **Feature Disparity**: Dataset 1 contains continuous age and clinical categories (`High`, `Normal`, `Low`); Dataset 2 contains only high-dimensional binary symptom indicators.
3. **Target Incompatibility**: Dataset 1 targets `Outcome Variable` (`Positive`/`Negative`), whereas Dataset 2 targets 391 distinct disease prognoses.
4. **Encoding Needs**: Dataset 1 requires categorical mapping from string (`'Yes'/'No'`, `'High'/'Low'`), whereas Dataset 2 features are already fully binary encoded integers.

### Recommendation
Keep Dataset 2 completely separate. Do not attempt to merge or concatenate with Dataset 1. Preserve `trainings.csv` and `testing.csv` in their original states as secondary lookup benchmarks for future specialized disease diagnostic modules.
