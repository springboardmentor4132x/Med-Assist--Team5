import csv
import math
from symptom_data import DATASET_FILE, COMMON_SYMPTOMS, SYMPTOMS, clean_name, make_label


# read the dataset once when the server starts
def load_rows():
    rows = []        # symptoms present in each row
    name_rows = {}   # symptom name -> set of row numbers that have it

    with open(DATASET_FILE, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = [clean_name(name) for name in next(reader)]

        for row in reader:
            if not row:
                continue

            number = len(rows)
            present = set()
            for name, value in zip(header, row):
                if value.strip() == "1" and name != "prognosis":
                    present.add(name)
                    name_rows.setdefault(name, set()).add(number)
            rows.append(present)

    return rows, name_rows


ROWS, NAME_ROWS = load_rows()
TOTAL_ROWS = len(ROWS)


# dataset columns of a symptom, "fever" means high_fever or mild_fever
def group_names(key):
    return COMMON_SYMPTOMS.get(key, [key])


# row numbers that have the symptom
def rows_with(key):
    found = set()
    for name in group_names(key):
        found = found | NAME_ROWS.get(name, set())
    return found


# fever, high_fever and mild_fever are the same kind of symptom,
# so if one is selected the others are not suggested
def family_names(key):
    names = set(group_names(key))
    names.add(key)

    for common, members in COMMON_SYMPTOMS.items():
        if key == common or key in members:
            names.add(common)
            names.update(members)

    return names


# phi coefficient, between -1 and 1
def phi_score(total, count_a, count_b, count_both):
    bottom = math.sqrt(count_a * (total - count_a) * count_b * (total - count_b))
    if bottom == 0:
        return 0.0
    return (total * count_both - count_a * count_b) / bottom


def strength_label(score):
    if score >= 0.5:
        return "strong"
    if score >= 0.3:
        return "moderate"
    if score >= 0.1:
        return "weak"
    return "none"


def percent(part, whole):
    if whole == 0:
        return 0.0
    return round(part * 100 / whole, 1)


def analyse_correlation(symptom_keys):
    sets = {}
    for key in symptom_keys:
        sets[key] = rows_with(key)

    # every pair of selected symptoms
    pairs = []
    for i in range(len(symptom_keys)):
        for j in range(i + 1, len(symptom_keys)):
            a = symptom_keys[i]
            b = symptom_keys[j]
            both = len(sets[a] & sets[b])
            score = phi_score(TOTAL_ROWS, len(sets[a]), len(sets[b]), both)

            pairs.append({
                "symptom_a": a,
                "symptom_a_label": SYMPTOMS[a],
                "symptom_b": b,
                "symptom_b_label": SYMPTOMS[b],
                "rows_together": both,
                "b_given_a": percent(both, len(sets[a])),
                "a_given_b": percent(both, len(sets[b])),
                "score": round(score, 2),
                "strength": strength_label(score),
            })

    strongest = None
    if pairs:
        strongest = max(pairs, key=lambda pair: pair["score"])

    # rows that have all the selected symptoms, if there are none use rows that have any of them
    based_on = "all_selected"
    base_rows = set.intersection(*sets.values()) if sets else set()
    if not base_rows:
        based_on = "any_selected"
        base_rows = set.union(*sets.values()) if sets else set()
    if not base_rows:
        based_on = "none"

    skip = set()
    for key in symptom_keys:
        skip = skip | family_names(key)

    # how many of those rows have each other symptom
    counts = {}
    for number in base_rows:
        for name in ROWS[number]:
            if name not in skip:
                counts[name] = counts.get(name, 0) + 1

    top = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]

    related = []
    for name, count in top:
        related.append({
            "key": name,
            "label": make_label(name),
            "percent": percent(count, len(base_rows)),
            "rows": count,
        })

    return {
        "dataset_rows": TOTAL_ROWS,
        "pairs": pairs,
        "strongest_pair": strongest,
        "related_symptoms": related,
        "related_based_on": based_on,
        "rows_used": len(base_rows),
    }
