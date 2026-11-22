"""
MedAssist AI - Module 3: Data Preprocessing
Script: dataset/preprocessing/preprocess_dataset.py

Author: Prabhas Pondara (MedAssist AI Team 5)
Responsibility: Dataset Exploration & Data Preprocessing

Description:
    This script loads the raw patient profile & disease symptom dataset,
    validates the schema, removes exact duplicate records, normalizes
    categorical features, converts binary symptoms to 1/0 integers,
    standardizes column names to snake_case, and exports the clean
    dataset to dataset/processed/cleaned_disease_dataset.csv.

Usage:
    python dataset/preprocessing/preprocess_dataset.py
    python dataset/preprocessing/preprocess_dataset.py --input-file <path> --output-dir <path>
"""

import os
import sys
import argparse
from pathlib import Path
import pandas as pd


# Default relative file paths
DEFAULT_INPUT_FILE = Path("dataset") / "Disease_symptom_and_patient_profile_dataset.csv"
DEFAULT_OUTPUT_DIR = Path("dataset") / "processed"
DEFAULT_OUTPUT_FILE = "cleaned_disease_dataset.csv"

# Expected schema definitions
EXPECTED_COLUMNS = [
    "Disease",
    "Fever",
    "Cough",
    "Fatigue",
    "Difficulty Breathing",
    "Age",
    "Gender",
    "Blood Pressure",
    "Cholesterol Level",
    "Outcome Variable",
]

COLUMN_RENAME_MAP = {
    "Disease": "disease",
    "Fever": "fever",
    "Cough": "cough",
    "Fatigue": "fatigue",
    "Difficulty Breathing": "difficulty_breathing",
    "Age": "age",
    "Gender": "gender",
    "Blood Pressure": "blood_pressure",
    "Cholesterol Level": "cholesterol_level",
    "Outcome Variable": "outcome_variable",
}

SYMPTOM_COLUMNS = ["fever", "cough", "fatigue", "difficulty_breathing"]
BINARY_MAP = {"Yes": 1, "No": 0, "yes": 1, "no": 0}
OUTCOME_BINARY_MAP = {"Positive": 1, "Negative": 0, "positive": 1, "negative": 0}


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments with sensible project defaults."""
    parser = argparse.ArgumentParser(
        description="MedAssist AI - Dataset Preprocessing Pipeline"
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help=f"Path to raw input CSV (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Path to processed output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Filename of clean output CSV (default: {DEFAULT_OUTPUT_FILE})",
    )
    return parser.parse_args()


def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Safely load the raw dataset using pandas without modifying the original file.
    Validates file existence, non-emptiness, and expected column headers.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found at '{file_path}'. "
            "Please verify the file exists relative to the project root."
        )

    if file_path.stat().st_size == 0:
        raise ValueError(f"Input dataset at '{file_path}' is empty.")

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback encoding if non-utf8 characters are encountered
        df = pd.read_csv(file_path, encoding="latin1")

    # Validate schema
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Input dataset schema mismatch. Missing required columns: {missing_cols}"
        )

    return df


def preprocess_patient_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the complete preprocessing pipeline according to EDA findings:
    1. Removes exact duplicate rows (justified to prevent data leakage).
    2. Preserves conflicting feature profiles (retaining medical nuances).
    3. Standardizes column names to lowercase snake_case.
    4. Cleans and normalizes text fields (trims whitespace, standardizes casing).
    5. Converts symptoms ('Yes'/'No') to numeric binary integers (1/0).
    6. Preserves readable disease and outcome labels.
    7. Adds an explicit 'outcome_binary' column (1 for Positive, 0 for Negative).
    8. Validates data integrity before returning.
    """
    # Create an independent copy to protect original DataFrame
    df = df_raw.copy()

    # Step 1: Remove exact duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    duplicates_removed = initial_rows - len(df)

    # Step 2: Standardize column names to snake_case
    df = df.rename(columns=COLUMN_RENAME_MAP)

    # Step 3: Normalize categorical string fields (strip whitespace, standard title casing)
    for col in ["disease", "gender", "blood_pressure", "cholesterol_level", "outcome_variable"]:
        df[col] = df[col].astype(str).str.strip()

    # Standardize specific text casing
    df["gender"] = df["gender"].str.capitalize()  # 'Female', 'Male'
    df["blood_pressure"] = df["blood_pressure"].str.capitalize()  # 'Low', 'Normal', 'High'
    df["cholesterol_level"] = df["cholesterol_level"].str.capitalize()  # 'Low', 'Normal', 'High'
    df["outcome_variable"] = df["outcome_variable"].str.capitalize()  # 'Positive', 'Negative'

    # Step 4: Convert symptom columns to 1/0 integers
    for symptom in SYMPTOM_COLUMNS:
        df[symptom] = df[symptom].astype(str).str.strip().str.capitalize()
        invalid_symptoms = df[~df[symptom].isin(["Yes", "No"])]
        if not invalid_symptoms.empty:
            raise ValueError(
                f"Unexpected value in symptom column '{symptom}': "
                f"{invalid_symptoms[symptom].unique()}"
            )
        df[symptom] = df[symptom].map(BINARY_MAP).astype(int)

    # Step 5: Validate and enforce Age as positive integer
    df["age"] = pd.to_numeric(df["age"], errors="raise").astype(int)
    if (df["age"] < 0).any() or (df["age"] > 125).any():
        raise ValueError("Age values outside valid human range (0-125) detected.")

    # Step 6: Create secondary numeric target representation without losing readable label
    df["outcome_binary"] = df["outcome_variable"].map(OUTCOME_BINARY_MAP).astype(int)

    # Step 7: Order columns logically for team handoff
    final_column_order = [
        "disease",
        "fever",
        "cough",
        "fatigue",
        "difficulty_breathing",
        "age",
        "gender",
        "blood_pressure",
        "cholesterol_level",
        "outcome_variable",
        "outcome_binary",
    ]
    df = df[final_column_order]

    return df


def validate_processed_data(df_clean: pd.DataFrame, expected_rows: int = 300) -> dict:
    """
    Rigorously validates the processed dataset against quality constraints:
    - Row count equals 300.
    - Zero null or NaN values across all columns.
    - Zero duplicate rows.
    - Symptom columns strictly contain {0, 1}.
    - Outcome binary strictly contains {0, 1}.
    - Age is within valid medical bounds.
    """
    validation_results = {}

    # Check 1: Row count
    actual_rows = len(df_clean)
    validation_results["row_count"] = actual_rows
    if actual_rows != expected_rows:
        raise AssertionError(
            f"Validation Failed: Expected {expected_rows} rows, got {actual_rows}"
        )

    # Check 2: Null values
    total_nulls = int(df_clean.isnull().sum().sum())
    validation_results["null_count"] = total_nulls
    if total_nulls != 0:
        raise AssertionError(
            f"Validation Failed: Found {total_nulls} null values in clean dataset."
        )

    # Check 3: Duplicates
    duplicate_count = int(df_clean.duplicated().sum())
    validation_results["duplicate_count"] = duplicate_count
    if duplicate_count != 0:
        raise AssertionError(
            f"Validation Failed: Found {duplicate_count} duplicate rows in clean dataset."
        )

    # Check 4: Symptom binary domains
    for col in SYMPTOM_COLUMNS:
        unique_vals = set(df_clean[col].unique())
        if not unique_vals.issubset({0, 1}):
            raise AssertionError(
                f"Validation Failed: Non-binary values {unique_vals} found in symptom '{col}'."
            )

    # Check 5: Target domain
    outcome_vals = set(df_clean["outcome_variable"].unique())
    if outcome_vals != {"Positive", "Negative"}:
        raise AssertionError(
            f"Validation Failed: Unexpected values in outcome_variable: {outcome_vals}"
        )

    # Check 6: Conflicting profiles preserved
    features = SYMPTOM_COLUMNS + ["age", "gender", "blood_pressure", "cholesterol_level"]
    grouped = df_clean.groupby(features)
    conflicting_outcome_groups = (grouped["outcome_variable"].nunique() > 1).sum()
    validation_results["conflicting_outcome_profiles"] = int(conflicting_outcome_groups)
    if conflicting_outcome_groups != 7:
        raise AssertionError(
            f"Validation Failed: Expected 7 preserved conflicting outcome profiles, found {conflicting_outcome_groups}."
        )

    return validation_results


def export_processed_data(df_clean: pd.DataFrame, output_dir: Path, output_file: str) -> Path:
    """Exports the cleaned DataFrame to CSV with directory creation and write confirmation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / output_file
    df_clean.to_csv(target_path, index=False, encoding="utf-8")
    return target_path


def main():
    """Main execution flow for preprocessing dataset."""
    args = parse_arguments()

    print("=" * 70)
    print("MEDASSIST AI - DATA PREPROCESSING PIPELINE (MODULE 3)")
    print("=" * 70)
    print(f"Loading raw dataset from:  {args.input_file}")

    try:
        df_raw = load_dataset(args.input_file)
    except Exception as e:
        print(f"[ERROR] Failed to load raw dataset: {e}", file=sys.stderr)
        sys.exit(1)

    raw_rows, raw_cols = df_raw.shape
    raw_dups = int(df_raw.duplicated().sum())
    raw_nulls = int(df_raw.isnull().sum().sum())

    print(f"[RAW DATA] Rows: {raw_rows} | Columns: {raw_cols}")
    print(f"[RAW DATA] Exact Duplicate Rows: {raw_dups}")
    print(f"[RAW DATA] Missing Cells: {raw_nulls}")

    print("\nExecuting preprocessing transformations...")
    try:
        df_clean = preprocess_patient_data(df_raw)
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nValidating processed dataset...")
    try:
        val_stats = validate_processed_data(df_clean, expected_rows=300)
    except AssertionError as e:
        print(f"[ERROR] Preprocessing validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[VALIDATION PASSED] Clean Rows: {val_stats['row_count']}")
    print(f"[VALIDATION PASSED] Clean Columns: {df_clean.shape[1]}")
    print(f"[VALIDATION PASSED] Null Count: {val_stats['null_count']}")
    print(f"[VALIDATION PASSED] Duplicate Count: {val_stats['duplicate_count']}")
    print(f"[VALIDATION PASSED] Conflicting Profiles Preserved: {val_stats['conflicting_outcome_profiles']}")

    # Export clean CSV
    try:
        target_path = export_processed_data(df_clean, args.output_dir, args.output_file)
        print(f"\n[EXPORT SUCCESS] Clean dataset saved to: {target_path}")
    except Exception as e:
        print(f"[ERROR] Failed to export processed dataset: {e}", file=sys.stderr)
        sys.exit(1)

    # Print summary statistics
    print("\n" + "=" * 70)
    print("PREPROCESSING SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Original shape:            ({raw_rows}, {raw_cols})")
    print(f"Processed shape:           ({df_clean.shape[0]}, {df_clean.shape[1]})")
    print(f"Exact duplicates removed:  {raw_dups}")
    print(f"Missing values remaining:  0")
    print(f"Binary symptom encoding:   fever, cough, fatigue, difficulty_breathing mapped to 1/0")
    print(f"Outcome target balance:    {dict(df_clean['outcome_variable'].value_counts())}")
    print(f"Binary target balance:     {dict(df_clean['outcome_binary'].value_counts())}")
    print("=" * 70)


if __name__ == "__main__":
    main()
