# MedAssist AI - Module 4, Member 4: Risk Categorization

```
MedAssist_Risk_Categorization/
├── backend/
│   ├── risk_categorization/     <- the component (drop into the real backend)
│   │   ├── constants.py         thresholds, priorities, labels/colours
│   │   ├── rules.py             pure categorization logic
│   │   ├── schemas.py           input/output models (Pydantic v2)
│   │   ├── explanations.py      explanation / guidance / emergency text
│   │   ├── service.py           categorize_risk()
│   │   ├── router.py            POST /api/risk/categorization
│   │   └── tests/
│   ├── dev_server.py            local demo server only
│   └── requirements.txt
└── frontend/                    plain HTML/CSS/JS demo UI (no build step)
    ├── index.html  style.css  app.js
```

## Run locally
Backend (from `backend/`):
    pip install -r requirements.txt
    uvicorn dev_server:app --reload --port 8000
    pytest risk_categorization/tests

Frontend (from `frontend/`):
    python -m http.server 5500     # then open http://localhost:5500
`API_BASE_URL` is at the top of `frontend/app.js`.

## Integration (Member 5)
    from risk_categorization.router import router
    app.include_router(router)
Add the project's auth dependency to the router if routes are protected.
Do not use dev_server.py (open CORS) in the real app.
Frontend team: copy the render logic from `frontend/app.js` into the real UI.

Results are preliminary automated estimates, not medical diagnoses. Thresholds
are demonstration values, not clinically validated.
