from models import get_db
from symptom_data import SYMPTOMS, COMMON_SYMPTOMS


# words that show a history record is about a selected symptom
def symptom_phrases(key):
    phrases = [SYMPTOMS[key].lower(), key.replace("_", " ")]
    for name in COMMON_SYMPTOMS.get(key, []):
        phrases.append(name.replace("_", " "))
    return phrases


def get_history_info(user_id, symptom_keys):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, condition, notes, record_date FROM medical_history WHERE user_id = ? ORDER BY record_date DESC, id DESC",
        (user_id,),
    ).fetchall()
    conn.close()

    all_records = []
    relevant_records = []

    for row in rows:
        record = dict(row)
        text = (record["condition"] + " " + (record["notes"] or "")).lower()

        matched = []
        for key in symptom_keys:
            for phrase in symptom_phrases(key):
                if phrase in text and SYMPTOMS[key] not in matched:
                    matched.append(SYMPTOMS[key])

        record["relevant"] = len(matched) > 0
        record["matched_symptoms"] = matched

        all_records.append(record)
        if record["relevant"]:
            relevant_records.append(record)

    return {
        "total_records": len(all_records),
        "relevant_count": len(relevant_records),
        "relevant_records": relevant_records,
        "all_records": all_records,
    }
