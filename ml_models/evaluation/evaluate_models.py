"""
MedAssist AI - Module 3: Model Evaluation & Selection
Script: ml_models/evaluation/evaluate_models.py
Responsibility: Member 3 - Model Evaluation & Selection

What this script does (run train_models.py first):
    1. Loads the models trained by Member 2.
    2. Evaluates each model on the held-out test set:
           accuracy, precision, recall, F1-score, confusion matrix
           (+ top-3 accuracy for diseases, ROC-AUC for the outcome task)
    3. Runs repeated stratified cross-validation, because the test sets are
       tiny (45 and 60 rows) and a single split is too noisy to trust.
    4. Compares every model against a "always predict the most common
       class" baseline, so we can see whether a model learned anything.
    5. Looks at per-disease performance of the selected disease model.
    6. Selects the best model for each task and saves it for Member 4/5:
           ml_models/best_disease_model.joblib
           ml_models/best_outcome_model.joblib
           ml_models/model_selection.json
    7. Writes the reports and charts to ml_models/reports/

Usage (from the project root):
    python ml_models/evaluation/evaluate_models.py
"""

import json
import sys
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.base import clone  # noqa: E402
from sklearn.dummy import DummyClassifier  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ml_models.common import (  # noqa: E402
    FEATURE_COLS,
    ML_DIR,
    MODEL_LABELS,
    MODEL_NAMES,
    RANDOM_STATE,
    REPORTS_DIR,
    TASKS,
    TRAINED_DIR,
    build_model,
    cv_subset,
    encode_target,
    load_data,
    make_split,
    predict_labels,
    top_k_accuracy,
)

FIG_DIR = REPORTS_DIR / "figures"
CV_FOLDS = 5
CV_REPEATS = 3


# ------------------------------------------------------------- metrics
def metric_set(task, y_true, y_pred, proba, classes):
    """All metrics for one set of predictions."""
    if task == "outcome":
        m = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }
        m["roc_auc"] = (
            roc_auc_score(y_true, proba[:, 1]) if len(set(y_true)) == 2 else np.nan
        )
        return m
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "top3": top_k_accuracy(proba, classes, y_true, 3),
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def cross_validate(model, X, y, task):
    """Repeated stratified CV. Returns mean and std of every metric."""
    cv = RepeatedStratifiedKFold(
        n_splits=CV_FOLDS, n_repeats=CV_REPEATS, random_state=RANDOM_STATE
    )
    rows = []
    for tr, te in cv.split(X, y):
        m = clone(model)
        m.fit(X.iloc[tr], y[tr])
        proba = m.predict_proba(X.iloc[te])
        pred = m.classes_[proba.argmax(axis=1)]
        rows.append(metric_set(task, y[te], pred, proba, m.classes_))
    keys = rows[0].keys()
    return {k: (float(np.nanmean([r[k] for r in rows])),
                float(np.nanstd([r[k] for r in rows]))) for k in keys}


# --------------------------------------------------------------- plots
def plot_cv_bars(task, table, path):
    names = [MODEL_LABELS.get(n, n) for n in table]
    key = "top3" if task == "disease" else "f1"
    first = [table[n]["cv"]["accuracy"][0] for n in table]
    second = [table[n]["cv"][key][0] for n in table]
    second_label = "Top-3 accuracy" if task == "disease" else "F1-score"

    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(x - 0.2, first, 0.4, label="Accuracy")
    ax.bar(x + 0.2, second, 0.4, label=second_label)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Cross-validation score")
    title = "Disease" if task == "disease" else "Outcome"
    ax.set_title(f"{title} task - cross-validated model comparison")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_confusion(cm, labels, title, path, size=(5, 4.5)):
    fig, ax = plt.subplots(figsize=size)
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(title)
    top = cm.max() / 2 if cm.max() else 1
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, int(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > top else "black", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------- evaluation
def evaluate_task(df, task):
    y, encoder = encode_target(df, task)
    train_idx, test_idx = make_split(df, y, task)
    X = df[FEATURE_COLS]
    X_test, y_test = X.iloc[test_idx], y[test_idx]
    X_cv, y_cv, cv_names = cv_subset(df, y, task, encoder)
    X_cv = X_cv[FEATURE_COLS]

    print(f"\n=== Task: {task} === (CV rows: {len(X_cv)}, classes: {len(cv_names)})")

    table = {}

    # baseline: always predict the most common class
    base_name = "baseline"
    base = Pipeline([("clf", DummyClassifier(strategy="prior"))])
    base_cv = cross_validate_dummy(base, X_cv, y_cv, task)
    table[base_name] = {"cv": base_cv, "holdout": None}

    for name in MODEL_NAMES:
        model = joblib.load(TRAINED_DIR / task / f"{name}.joblib")
        proba = model.predict_proba(X_test)
        pred = model.classes_[proba.argmax(axis=1)]
        holdout = metric_set(task, y_test, pred, proba, model.classes_)
        cm = confusion_matrix(y_test, pred, labels=model.classes_) if task == "outcome" else None

        cv = cross_validate(build_model(name, task), X_cv, y_cv, task)

        train_acc = float(np.mean(predict_labels(model, X.iloc[train_idx]) == y[train_idx]))
        table[name] = {
            "holdout": holdout,
            "cv": cv,
            "train_accuracy": train_acc,
            "confusion": cm,
        }
        key = "top3" if task == "disease" else "f1"
        print(f"  {MODEL_LABELS[name]:<20} holdout acc={holdout['accuracy']:.3f} | "
              f"CV acc={cv['accuracy'][0]:.3f} CV {key}={cv[key][0]:.3f}")

    return table, encoder, (X_cv, y_cv, cv_names), (train_idx, test_idx, y)


def cross_validate_dummy(model, X, y, task):
    """Same CV as cross_validate but the dummy baseline needs no features."""
    cv = RepeatedStratifiedKFold(
        n_splits=CV_FOLDS, n_repeats=CV_REPEATS, random_state=RANDOM_STATE
    )
    rows = []
    for tr, te in cv.split(X, y):
        m = clone(model)
        m.fit(X.iloc[tr], y[tr])
        proba = m.predict_proba(X.iloc[te])
        pred = m.classes_[proba.argmax(axis=1)]
        rows.append(metric_set(task, y[te], pred, proba, m.classes_))
    return {k: (float(np.nanmean([r[k] for r in rows])),
                float(np.nanstd([r[k] for r in rows]))) for k in rows[0]}


def select_best(task, table):
    """Selection rule (written in the report as well):
    disease -> highest CV top-3 accuracy (the app shows the top 3), then CV weighted F1
    outcome -> highest CV F1-score, then CV ROC-AUC
    """
    if task == "disease":
        order = lambda n: (table[n]["cv"]["top3"][0], table[n]["cv"]["f1"][0])
    else:
        order = lambda n: (table[n]["cv"]["f1"][0], table[n]["cv"]["roc_auc"][0])
    ranked = sorted(MODEL_NAMES, key=order, reverse=True)
    return ranked[0], ranked


def per_disease_report(best_name, X_cv, y_cv, cv_names):
    """Out-of-fold predictions for the selected disease model, so each
    disease is judged on rows the model has not seen."""
    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    oof = np.zeros_like(y_cv)
    for tr, te in skf.split(X_cv, y_cv):
        m = build_model(best_name, "disease")
        m.fit(X_cv.iloc[tr], y_cv[tr])
        oof[te] = predict_labels(m, X_cv.iloc[te])
    rep = classification_report(
        y_cv, oof, labels=range(len(cv_names)), target_names=cv_names,
        output_dict=True, zero_division=0,
    )
    return rep, oof


# -------------------------------------------------------------- report
def fmt(pair, digits=3):
    mean, std = pair
    return f"{mean:.{digits}f} ± {std:.{digits}f}"


def build_report(results, selection, per_disease):
    L = []
    L += [
        "# Model Evaluation & Selection Report",
        "## MedAssist AI - Module 3 (Member 3: Model Evaluation & Selection)",
        "",
        "Generated by `ml_models/evaluation/evaluate_models.py` from the models",
        "trained by `ml_models/training/train_models.py`.",
        "",
        "> MedAssist AI is a preliminary decision-support tool. Scores below",
        "> describe model behaviour on a small dataset; they are not medical",
        "> certainty and the predictions are not diagnoses.",
        "",
        "## 1. How the models were evaluated",
        "",
        "- **Hold-out test set** (20% of the data, `random_state=42`): used for",
        "  accuracy, precision, recall, F1-score and the confusion matrix.",
        "  Only 45 rows (disease) and 60 rows (outcome), so one wrong prediction",
        "  moves accuracy by 1.7-2.2 points. It is a sanity check, not a verdict.",
        f"- **Repeated stratified cross-validation** ({CV_FOLDS} folds x {CV_REPEATS} repeats):",
        "  each model is retrained 15 times on different splits and scores are",
        "  averaged (mean ± standard deviation). **Model selection uses this.**",
        "- **Baseline**: a dummy model that always predicts the most common class.",
        "  A real model must clearly beat it to be worth using.",
        "- Disease cross-validation uses only the 28 diseases that have at least",
        f"  {5} records (195 rows). Diseases with 1-4 records cannot be split across",
        "  five folds. The hold-out test still uses all 116 disease labels.",
        "- For diseases, precision/recall/F1 are **weighted** averages (weighted by",
        "  how many records each disease has); macro F1 is also shown.",
        "",
    ]

    for task, title in (("disease", "Disease classification"),
                        ("outcome", "Outcome classification (Positive / Negative)")):
        table = results[task]["table"]
        best, ranked = selection[task]
        n = "2" if task == "disease" else "3"
        L += [f"## {n}. {title}", ""]

        # cross-validation table
        L += ["### Cross-validation results (used for selection)", ""]
        if task == "disease":
            L += ["| Rank | Model | Accuracy | Top-3 accuracy | Precision (w) | Recall (w) | F1 (w) | Macro F1 |",
                  "| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
            for i, name in enumerate(ranked, 1):
                c = table[name]["cv"]
                L.append(f"| {i} | {MODEL_LABELS[name]} | {fmt(c['accuracy'])} | {fmt(c['top3'])} | "
                         f"{fmt(c['precision'])} | {fmt(c['recall'])} | {fmt(c['f1'])} | {fmt(c['macro_f1'])} |")
            c = table["baseline"]["cv"]
            L.append(f"| - | Baseline (most common) | {fmt(c['accuracy'])} | {fmt(c['top3'])} | "
                     f"{fmt(c['precision'])} | {fmt(c['recall'])} | {fmt(c['f1'])} | {fmt(c['macro_f1'])} |")
        else:
            L += ["| Rank | Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |",
                  "| ---: | :--- | ---: | ---: | ---: | ---: | ---: |"]
            for i, name in enumerate(ranked, 1):
                c = table[name]["cv"]
                L.append(f"| {i} | {MODEL_LABELS[name]} | {fmt(c['accuracy'])} | {fmt(c['precision'])} | "
                         f"{fmt(c['recall'])} | {fmt(c['f1'])} | {fmt(c['roc_auc'])} |")
            c = table["baseline"]["cv"]
            L.append(f"| - | Baseline (most common) | {fmt(c['accuracy'])} | {fmt(c['precision'])} | "
                     f"{fmt(c['recall'])} | {fmt(c['f1'])} | {fmt(c['roc_auc'])} |")
        L += ["", f"![CV comparison](figures/{task}_cv_comparison.png)", ""]

        # hold-out table
        L += ["### Hold-out test results", ""]
        if task == "disease":
            L += ["| Model | Train acc. | Test acc. | Test top-3 | Precision (w) | Recall (w) | F1 (w) | Macro F1 |",
                  "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
            for name in MODEL_NAMES:
                h = table[name]["holdout"]
                L.append(f"| {MODEL_LABELS[name]} | {table[name]['train_accuracy']:.3f} | {h['accuracy']:.3f} | "
                         f"{h['top3']:.3f} | {h['precision']:.3f} | {h['recall']:.3f} | {h['f1']:.3f} | {h['macro_f1']:.3f} |")
        else:
            L += ["| Model | Train acc. | Test acc. | Precision | Recall | F1-score | ROC-AUC |",
                  "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
            for name in MODEL_NAMES:
                h = table[name]["holdout"]
                L.append(f"| {MODEL_LABELS[name]} | {table[name]['train_accuracy']:.3f} | {h['accuracy']:.3f} | "
                         f"{h['precision']:.3f} | {h['recall']:.3f} | {h['f1']:.3f} | {h['roc_auc']:.3f} |")
        L.append("")

        if task == "outcome":
            L += ["### Confusion matrices (hold-out, 60 rows)", "",
                  "Rows = actual, columns = predicted (0 = Negative, 1 = Positive).", "",
                  "| Model | True Neg | False Pos | False Neg | True Pos |",
                  "| :--- | ---: | ---: | ---: | ---: |"]
            for name in MODEL_NAMES:
                cm = table[name]["confusion"]
                L.append(f"| {MODEL_LABELS[name]} | {cm[0,0]} | {cm[0,1]} | {cm[1,0]} | {cm[1,1]} |")
            L += ["", "![Confusion matrices](figures/outcome_confusion_matrices.png)", ""]

        # selection
        c = table[best]["cv"]
        L += ["### Selected model", "",
              f"**{MODEL_LABELS[best]}**", ""]
        if task == "disease":
            L += ["Selection rule: highest cross-validated **top-3 accuracy** (the app",
                  "shows the three most likely diseases), then weighted F1.", ""]
        else:
            L += ["Selection rule: highest cross-validated **F1-score**, then ROC-AUC.",
                  "Recall is reported next to precision because in a health setting a",
                  "missed positive case is the more costly mistake.", ""]
        L += [results[task]["reason"], ""]

    # per disease
    rep, names, best = per_disease
    L += ["## 4. Per-disease performance of the selected disease model", "",
          f"Out-of-fold predictions ({CV_FOLDS}-fold) of **{MODEL_LABELS[best]}** on the 28",
          "diseases that have at least 5 records. Accuracy alone hides this: a model",
          "can look fine while never predicting the rarer diseases.", "",
          "| Disease | Records | Precision | Recall | F1-score |",
          "| :--- | ---: | ---: | ---: | ---: |"]
    order = sorted(names, key=lambda d: -rep[d]["support"])
    for d in order:
        r = rep[d]
        L.append(f"| {d} | {int(r['support'])} | {r['precision']:.2f} | {r['recall']:.2f} | {r['f1-score']:.2f} |")
    never = [d for d in names if rep[d]["recall"] == 0]
    L += ["",
          f"Diseases the model never predicted correctly: {len(never)} of {len(names)}"
          + (f" ({', '.join(never)})." if never else "."),
          "",
          "![Confusion matrix of the 10 most common diseases](figures/disease_confusion_top10.png)",
          ""]

    # key findings (numbers are filled in from the results above)
    td, to = results["disease"]["table"], results["outcome"]["table"]
    bd, bo = selection["disease"][0], selection["outcome"][0]
    cd, co = td[bd]["cv"], to[bo]["cv"]
    L += [
        "## 5. Key findings and limitations", "",
        f"- **Outcome model works moderately.** {MODEL_LABELS[bo]} reaches CV accuracy "
        f"{co['accuracy'][0]:.2f} and F1 {co['f1'][0]:.2f}, against "
        f"{to['baseline']['cv']['accuracy'][0]:.2f} accuracy for always guessing the most common class. "
        "There is real signal, but roughly one prediction in four is still wrong.",
        f"- **Disease model is weak.** {MODEL_LABELS[bd]} reaches CV top-1 accuracy {cd['accuracy'][0]:.2f} "
        f"and top-3 accuracy {cd['top3'][0]:.2f}; the baseline gets {td['baseline']['cv']['accuracy'][0]:.2f} "
        f"and {td['baseline']['cv']['top3'][0]:.2f}. It beats the baseline only slightly, and "
        f"{len(never)} of {len(names)} diseases are never predicted correctly. "
        "No algorithm fixes this: the data has only 4 symptoms plus age, gender, blood pressure and "
        "cholesterol for 116 diseases and 300 rows (77 of the 116 diseases appear only once and 88 have fewer than 5 records), which is "
        "not enough to tell the diseases apart. Prabhas noted the same risk in TEAM_HANDOFF.md (section 5.2).",
        "- **Overfitting.** Decision Tree and Random Forest score far higher on training data than on "
        "unseen data for the disease task. Do not quote training accuracy anywhere.",
        "- **Scores are not medical probabilities.** Random Forest probabilities are averaged tree votes "
        "and are low and flat for 116 classes. Member 4 should present them as relative model scores "
        "(for ranking the top 3), not as the chance that the person has the disease.",
        "- **Possible improvement (team decision).** The second recommended dataset "
        "(`trainings.csv` / `testing.csv`, many binary symptoms) is much better suited to symptom-to-disease "
        "prediction. It has a different schema and must not be merged with this one, but the disease task "
        "could be trained on it separately.",
        "",
        "## 6. Files for Member 4 and Member 5", "",
        "| File | Purpose |", "| :--- | :--- |",
        "| `ml_models/best_disease_model.joblib` | Selected disease pipeline (raw columns in, probabilities out) |",
        "| `ml_models/best_disease_label_encoder.joblib` | Turns class ids back into disease names |",
        "| `ml_models/best_outcome_model.joblib` | Selected Positive/Negative pipeline |",
        "| `ml_models/best_outcome_label_encoder.joblib` | Class ids for the outcome model (0 = Negative, 1 = Positive) |",
        "| `ml_models/model_selection.json` | Selected model names, feature columns and CV scores |",
        "",
        "The selected algorithms were refitted on all 300 cleaned rows before saving, so the",
        "disease model knows all 116 diseases. The scores in this report come from",
        "cross-validation and hold-out testing, not from that final refit.",
        "",
        "```python",
        "import joblib, pandas as pd",
        "model = joblib.load('ml_models/best_disease_model.joblib')",
        "encoder = joblib.load('ml_models/best_disease_label_encoder.joblib')",
        "",
        "patient = pd.DataFrame([{",
        "    'fever': 1, 'cough': 0, 'fatigue': 1, 'difficulty_breathing': 0,",
        "    'age': 35, 'gender': 'Male', 'blood_pressure': 'Normal', 'cholesterol_level': 'Normal',",
        "}])",
        "proba = model.predict_proba(patient)[0]",
        "top3 = proba.argsort()[::-1][:3]",
        "for i in top3:",
        "    print(encoder.inverse_transform([model.classes_[i]])[0], round(float(proba[i]), 3))",
        "```",
        "",
        "Column names, 0/1 symptom values and category spellings must match the cleaned dataset",
        "(`gender`: Female/Male; `blood_pressure` and `cholesterol_level`: Low/Normal/High).",
        "",
        "## 7. How to re-run", "",
        "```bash",
        "python ml_models/training/train_models.py",
        "python ml_models/evaluation/evaluate_models.py",
        "```",
        "",
    ]
    return L


def main():
    print("=" * 70)
    print("MEDASSIST AI - MODEL EVALUATION & SELECTION (MODULE 3, MEMBER 3)")
    print("=" * 70)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    results, selection = {}, {}
    for task in TASKS:
        if not (TRAINED_DIR / task).exists():
            sys.exit("Trained models not found. Run ml_models/training/train_models.py first.")
        table, encoder, cv_data, split = evaluate_task(df, task)
        best, ranked = select_best(task, table)
        selection[task] = (best, ranked)
        results[task] = {"table": table, "encoder": encoder, "cv_data": cv_data, "split": split}

        plot_cv_bars(task, {n: table[n] for n in ranked}, FIG_DIR / f"{task}_cv_comparison.png")

    # ---- outcome confusion matrices (all models) ----
    table = results["outcome"]["table"]
    fig, axes = plt.subplots(1, len(MODEL_NAMES), figsize=(3.2 * len(MODEL_NAMES), 3.4))
    for ax, name in zip(axes, MODEL_NAMES):
        cm = table[name]["confusion"]
        ax.imshow(cm, cmap="Blues")
        ax.set_title(MODEL_LABELS[name], fontsize=9)
        ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xticklabels(["Neg", "Pos"]); ax.set_yticklabels(["Neg", "Pos"])
        ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
        for i in range(2):
            for j in range(2):
                ax.text(j, i, int(cm[i, j]), ha="center", va="center",
                        color="white" if cm[i, j] > cm.max() / 2 else "black")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "outcome_confusion_matrices.png", dpi=130)
    plt.close(fig)

    # ---- explanations for why each winner was chosen ----
    for task in TASKS:
        best, ranked = selection[task]
        t = results[task]["table"]
        base = t["baseline"]["cv"]
        c = t[best]["cv"]
        runner = ranked[1]
        r = t[runner]["cv"]
        gap = t[best]["train_accuracy"] - t[best]["holdout"]["accuracy"]
        key = "top3" if task == "disease" else "f1"
        label = "top-3 accuracy" if task == "disease" else "F1-score"
        txt = (f"- CV {label}: {c[key][0]:.3f} for {MODEL_LABELS[best]} vs "
               f"{r[key][0]:.3f} for the runner-up ({MODEL_LABELS[runner]}) and "
               f"{base[key][0]:.3f} for the baseline.\n"
               f"- CV accuracy: {c['accuracy'][0]:.3f} (baseline {base['accuracy'][0]:.3f}).\n"
               f"- Train accuracy minus hold-out accuracy: {gap:+.3f} "
               f"({'noticeable overfitting' if gap > 0.15 else 'small gap, no strong overfitting'}).")
        if c[key][0] - r[key][0] < c[key][1] + r[key][1]:
            txt += ("\n- The difference to the runner-up is smaller than the fold-to-fold "
                    "spread, so the top models are statistically close; "
                    f"{MODEL_LABELS[best]} is chosen because it ranks first by the rule above.")
        results[task]["reason"] = txt

    # ---- per-disease analysis for the selected disease model ----
    best_d = selection["disease"][0]
    X_cv, y_cv, names = results["disease"]["cv_data"]
    rep, oof = per_disease_report(best_d, X_cv, y_cv, names)
    counts = np.bincount(y_cv)
    top10 = np.argsort(-counts)[:10]
    mask = np.isin(y_cv, top10)
    cm = confusion_matrix(y_cv[mask], oof[mask], labels=top10)
    plot_confusion(cm, [names[i] for i in top10],
                   f"{MODEL_LABELS[best_d]} - 10 most common diseases (out-of-fold)",
                   FIG_DIR / "disease_confusion_top10.png", size=(8, 7))

    # ---- write the evaluation report ----
    lines = build_report(results, selection, (rep, list(names), best_d))
    (REPORTS_DIR / "model_evaluation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- final models: refit selected algorithm on all rows, save ----
    meta = {}
    for task in TASKS:
        best, ranked = selection[task]
        y, encoder = encode_target(df, task)
        final = build_model(best, task)
        final.fit(df[FEATURE_COLS], y)
        out = ML_DIR / f"best_{task}_model.joblib"
        joblib.dump(final, out)
        joblib.dump(encoder, ML_DIR / f"best_{task}_label_encoder.joblib")
        c = results[task]["table"][best]["cv"]
        meta[task] = {
            "selected_model": best,
            "model_file": out.name,
            "label_encoder_file": f"best_{task}_label_encoder.joblib",
            "feature_columns": FEATURE_COLS,
            "n_classes": int(len(encoder.classes_)),
            "ranking": ranked,
            "cv_metrics": {k: round(v[0], 4) for k, v in c.items()},
            "note": "Selected algorithm refitted on all cleaned rows. Scores come from "
                    "cross-validation, not from this refit. Preliminary decision-support only.",
        }
        print(f"\nSelected for {task}: {MODEL_LABELS[best]}  ->  {out.name}")
    (ML_DIR / "model_selection.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("\nReport:", REPORTS_DIR / "model_evaluation_report.md")


if __name__ == "__main__":
    main()
