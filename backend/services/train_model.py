import pandas as pd

# Load the cleaned dataset
file_path = "dataset/cleaned_disease_dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 records:")
print(df.head())

print("\nTarget column distribution:")
print(df["Outcome Variable"].value_counts())
# Separate input features and target

X = df[
    [
        "Fever",
        "Cough",
        "Fatigue",
        "Difficulty Breathing",
        "Age",
        "Gender",
        "Blood Pressure",
        "Cholesterol Level"
    ]
]

y = df["Outcome Variable"]

print("\n--- INPUT FEATURES ---")
print(X.head())

print("\n--- TARGET VALUES ---")
print(y.head())

print("\nNumber of input features:", X.shape[1])
print("Number of target records:", y.shape[0])
# Convert categorical input features into numerical values

X_encoded = pd.get_dummies(
    X,
    columns=[
        "Fever",
        "Cough",
        "Fatigue",
        "Difficulty Breathing",
        "Gender",
        "Blood Pressure",
        "Cholesterol Level"
    ],
    dtype=int
)

# Convert target labels into numbers
y_encoded = y.map({
    "Negative": 0,
    "Positive": 1
})

print("\n--- ENCODED INPUT FEATURES ---")
print(X_encoded.head())

print("\n--- ENCODED TARGET ---")
print(y_encoded.head())

print("\nTotal numerical features:", X_encoded.shape[1])
from sklearn.model_selection import train_test_split

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("\n--- TRAINING AND TESTING DATA ---")

print("Training input records:", X_train.shape[0])
print("Testing input records:", X_test.shape[0])

print("Training target records:", y_train.shape[0])
print("Testing target records:", y_test.shape[0])
from sklearn.ensemble import RandomForestClassifier

# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

print("\n--- MODEL TRAINING ---")
print("Random Forest model trained successfully!")

# Check accuracy on training and testing data
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print("\nTraining accuracy:", train_accuracy)
print("Testing accuracy:", test_accuracy)
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

# Make predictions on testing data
y_pred = model.predict(X_test)

print("\n--- MODEL EVALUATION ---")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Negative", "Positive"]
))
import joblib

# Save the trained model
joblib.dump(model, "ml_models/random_forest_model.pkl")

print("\nModel saved successfully!")
