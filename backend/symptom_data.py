import csv
import os
from config import BASE_DIR

# symptoms of the dataset are the column names of this file
DATASET_FILE = os.path.join(BASE_DIR, "data", "Training.csv")

MAX_SYMPTOMS = 20

# names that people use normally, mapped to the symptom columns of the dataset
COMMON_SYMPTOMS = {
    "fever": ["high_fever", "mild_fever"],
    "body_pain": ["muscle_pain", "joint_pain"],
    "sore_throat": ["throat_irritation"],
    "difficulty_breathing": ["breathlessness"],
}

# shown at the top of the symptom page
QUICK_SYMPTOMS = [
    "fever", "headache", "cough", "body_pain", "fatigue",
    "nausea", "vomiting", "sore_throat", "difficulty_breathing",
]


# some column names in the file have spaces, like "spotting_ urination"
def clean_name(name):
    return name.strip().replace("_ ", "_").replace(" _", "_").replace(" ", "_").lower()


def load_columns():
    columns = {}
    with open(DATASET_FILE, newline="", encoding="utf-8") as file:
        header = next(csv.reader(file))

    for name in header:
        if name.strip() == "" or name.strip().lower() == "prognosis" or name.startswith("Unnamed"):
            continue
        columns[clean_name(name)] = name

    return columns


# clean name -> real column name in the csv file
DATASET_COLUMNS = load_columns()


def make_label(key):
    return key.replace("_", " ").capitalize()


# all symptoms that a user can select: key -> label
SYMPTOMS = {}
for key in DATASET_COLUMNS:
    SYMPTOMS[key] = make_label(key)
for key in COMMON_SYMPTOMS:
    SYMPTOMS[key] = make_label(key)


# real csv column names of a symptom
def get_dataset_columns(key):
    if key in COMMON_SYMPTOMS:
        return [DATASET_COLUMNS[name] for name in COMMON_SYMPTOMS[key]]
    return [DATASET_COLUMNS[key]]
