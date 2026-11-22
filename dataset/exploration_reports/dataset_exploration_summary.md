# Dataset Exploration Phase 1: Summary & Handoff
## MedAssist AI – Module 3 Data Engineering & Exploration
**Module Status:** Phase 1 (Dataset Exploration) Completed  
**Generated Date:** 2026-11-22  
**Reporting Engineer:** Prabhas Pondara  
**Repository Branch:** `feature/Prabhas-patient-profile-management`

---

## 1. Overview of Phase 1 Completion

Phase 1 (Dataset Exploration) for Module 3 has been completed. All four candidate CSV files in the `dataset/` directory were independently inspected, verified, and analyzed.

The following four comprehensive exploration reports have been generated in `dataset/exploration_reports/`:

1. [dataset1_exploration_report.md](file:///c:/INFOSYS/Med-Assist--Team5/dataset/exploration_reports/dataset1_exploration_report.md) – Detailed EDA on `Disease_symptom_and_patient_profile_dataset.csv` and `cleaned_disease_dataset.csv`.
2. [dataset2_exploration_report.md](file:///c:/INFOSYS/Med-Assist--Team5/dataset/exploration_reports/dataset2_exploration_report.md) – Detailed EDA on `trainings.csv` and `testing.csv`.
3. [dataset_comparison_report.md](file:///c:/INFOSYS/Med-Assist--Team5/dataset/exploration_reports/dataset_comparison_report.md) – Side-by-side comparison, schema compatibility assessment, and architectural recommendations.
4. [dataset_exploration_summary.md](file:///c:/INFOSYS/Med-Assist--Team5/dataset/exploration_reports/dataset_exploration_summary.md) – Executive synthesis and Phase 2 transition plan.

---

## 2. Master Verification Table Across All CSV Files

| Metric | Raw Dataset (`Disease_symptom...`) | Existing Cleaned (`cleaned_disease...`) | Trainings Dataset (`trainings.csv`) | Testing Dataset (`testing.csv`) |
| :--- | :---: | :---: | :---: | :---: |
| **Row Count** | **349** | **300** | **391** | **414** |
| **Column Count** | **10** | **10** | **1,327** | **1,327** |
| **Missing Cells** | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **Duplicate Rows** | 49 (14.04%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **Feature Domain** | Demographics, Vitals, 4 Symptoms | Demographics, Vitals, 4 Symptoms | 1,326 Binary Symptoms | 1,326 Binary Symptoms |
| **Target Column** | `Outcome Variable` / `Disease` | `Outcome Variable` / `Disease` | `Prognosis` | `Prognosis` |
| **Target Unique Classes**| 2 (`Outcome`) / 116 (`Disease`) | 2 (`Outcome`) / 116 (`Disease`) | 391 unique diseases | 389 unique diseases |
| **Matrix Density** | Dense (100% filled) | Dense (100% filled) | Ultra-sparse (>99.4% zeros) | Ultra-sparse (>99.3% zeros) |
| **Encoding** | Clean UTF-8 | Clean UTF-8 | Latin-1 (Byte `0xa0`) | Latin-1 (Byte `0xa0`) |
| **Application Match** | **Direct Match** | **Direct Match** | High-dimensional reference | High-dimensional reference |

---

## 3. Critical Verified Insights

### 3.1 Equivalence of `cleaned_disease_dataset.csv`
- Verification confirmed that `cleaned_disease_dataset.csv` is mathematically identical to `df_raw.drop_duplicates()`.
- No feature normalization, encoding, or schema renaming has been applied to it yet.

### 3.2 49 Exact Duplicate Records
- All 49 duplicate rows are verbatim copies across all 10 fields simultaneously.
- Dropping these duplicates is statistically necessary to avoid biased performance metrics and artificial data leakage.

### 3.3 Clinical Overlaps & Conflicting Outcomes
- **45 Feature Profiles with Multiple Diseases**: 45 combinations of the 8 features correspond to two or more distinct medical conditions (demonstrating symptom overlap common in clinical practice).
- **7 Feature Profiles with Conflicting Outcomes**: Exactly 7 feature combinations (16 total rows) have identical symptom and demographic inputs but opposing `Outcome Variable` values (`Positive` vs `Negative`).
- **Modeling Implication**: Establishes an irreducible Bayes error floor of $\approx 2.33\%$ when predicting `Outcome Variable` without knowing the specific underlying disease.

### 3.4 Schema Incompatibility Between Datasets
- Merging `Disease_symptom_and_patient_profile_dataset.csv` with `trainings.csv` or `testing.csv` is **impossible and prohibited**:
  - Columns do not match (10 vs 1,327).
  - Demographics are absent in Dataset 2.
  - Only 33 diseases overlap between the two collections.
  - Dataset 2 must remain an independent reference lookup dataset.

---

## 4. Architectural Selection for MedAssist AI

### Primary Dataset Selected: `Disease_symptom_and_patient_profile_dataset.csv`
This dataset is selected as the primary dataset for the MedAssist AI platform because:
1. It contains the exact features gathered in the patient profile and symptom intake forms (`Age`, `Gender`, `Blood Pressure`, `Cholesterol Level`, `Fever`, `Cough`, `Fatigue`, `Difficulty Breathing`).
2. It matches the signature of the pre-trained model `ml_models/random_forest_model.pkl` loaded by `backend/services/predict.py`.
3. It has a balanced binary target (52.3% Positive vs 47.7% Negative), providing a solid base for risk stratification.

---

## 5. Transition Plan for Phase 2 (Data Preprocessing)

When approved to begin Phase 2, the following pipeline will be implemented:

1. **Preprocessing Script (`dataset/preprocessing/preprocess_dataset.py`)**:
   - Reusable, documented, relative-path script.
   - Loads `Disease_symptom_and_patient_profile_dataset.csv` without modifying the original.
   - Removes the 49 duplicates.
   - Converts symptom strings (`Yes`/`No`) to integer binary indicators (`1`/`0`).
   - Converts `Outcome Variable` (`Positive`/`Negative`) to integer binary flags (`1`/`0`).
   - Standardizes column names to `lower_snake_case`.
   - Normalizes text values to trimmed lowercase.
2. **Processed Dataset**:
   - Export to `dataset/processed/cleaned_disease_dataset.csv`.
3. **Team Documentation**:
   - Save audit logs in `dataset/processed/preprocessing_summary.md`.
   - Save handoff and loading instructions in `dataset/processed/TEAM_HANDOFF.md`.

---

## 6. Strict Compliance Checklist

- [x] All 4 EDA reports generated and stored in `dataset/exploration_reports/`.
- [x] All statistics independently calculated and verified directly from raw CSV files.
- [x] Original CSV files remain **100% untouched and preserved**.
- [x] No data preprocessing, duplicate removal, or file cleaning executed.
- [x] No machine learning model training or confidence score calculation performed.
- [x] No existing backend or frontend code modified.
- [x] No automated git commits or pushes executed.
- [x] Work halted pending user review and approval.
