import pandas as pd

file_path = "dataset/Disease_symptom_and_patient_profile_dataset.csv"

df = pd.read_csv(file_path)

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())
print("\n--- DISEASE COUNTS ---")
print(df["Disease"].value_counts())

print("\n--- OUTCOME COUNTS ---")
print(df["Outcome Variable"].value_counts())

print("\n--- UNIQUE VALUES IN SYMPTOM COLUMNS ---")
for column in ["Fever", "Cough", "Fatigue", "Difficulty Breathing"]:
    print(f"\n{column}:")
    print(df[column].value_counts())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())
print("\n--- SAMPLE DUPLICATE RECORDS ---")

duplicates = df[df.duplicated(keep=False)]

print(duplicates.sort_values(by="Disease").head(10).to_string(index=False))
# Create a cleaned copy without exact duplicate rows
cleaned_df = df.drop_duplicates()

# Save the cleaned dataset
cleaned_df.to_csv(
    "dataset/cleaned_disease_dataset.csv",
    index=False
)

print("\n--- CLEANING SUMMARY ---")
print("Original records:", len(df))
print("Records after removing duplicates:", len(cleaned_df))
print("Duplicates removed:", len(df) - len(cleaned_df))

print("\nCleaned dataset saved successfully!")
print("\n--- DISEASE RECORD DISTRIBUTION ---")

disease_counts = cleaned_df["Disease"].value_counts()

print("Total disease categories:", len(disease_counts))
print("\nDiseases with at least 5 records:")
print(disease_counts[disease_counts >= 5])

print("\nDiseases with fewer than 5 records:")
print(disease_counts[disease_counts < 5].shape[0])
