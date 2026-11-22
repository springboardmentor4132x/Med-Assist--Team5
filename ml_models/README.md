# ml_models - Module 3: Disease Prediction Models

MedAssist AI (Team 5). Work split inside Module 3:

| Part | Owner | Where |
| :--- | :--- | :--- |
| Dataset exploration & preprocessing | Member 1 (Prabhas) | `dataset/` |
| Model training | Member 2 | `ml_models/training/train_models.py` |
| Model evaluation & selection | Member 3 | `ml_models/evaluation/evaluate_models.py` |
| Prediction logic & confidence scoring | Member 4 | (next) |
| FastAPI integration & frontend | Member 5 | (next) |

## Run order (from the project root)

```bash
pip install pandas scikit-learn xgboost joblib matplotlib
python ml_models/training/train_models.py       # trains 5 models x 2 tasks
python ml_models/evaluation/evaluate_models.py  # compares, selects, saves best
```

## Two prediction tasks

| Task | Target | Classes | Why |
| :--- | :--- | ---: | :--- |
| `disease` | `disease` | 116 | What the module brief asks for (disease categories, top 3, probabilities) |
| `outcome` | `outcome_binary` | 2 | Well-conditioned target recommended in `dataset/processed/TEAM_HANDOFF.md` |

Models: Decision Tree, Random Forest, SVM (RBF), XGBoost, Logistic Regression.
Each saved model is a scikit-learn `Pipeline` that takes the raw patient columns
(`fever, cough, fatigue, difficulty_breathing, age, gender, blood_pressure, cholesterol_level`)
and does the encoding itself, so training and prediction always use the same preprocessing.

## Outputs

- `ml_models/best_disease_model.joblib`, `best_outcome_model.joblib` - selected models (used by Member 4/5)
- `ml_models/best_*_label_encoder.joblib` - class id -> name
- `ml_models/model_selection.json` - which model won and its scores
- `ml_models/reports/model_training_report.md` - training summary
- `ml_models/reports/model_evaluation_report.md` - metrics, confusion matrices, selection and reasons
- `ml_models/reports/figures/` - charts
- `ml_models/trained_models/` - all trained models (not committed; recreated by the training script)

`ml_models/random_forest_model.pkl` is the older single model used by
`backend/services/predict.py`; it is left untouched.

> Predictions are preliminary decision-support output, not medical diagnoses.
