"""
MedAssist AI - Disease Knowledge & Explanation Base
Inspired by the Human Symptoms-Disease Network (HSDN) research (Zhou et al., Nature Communications).
Provides clinical etiology (causes), pathophysiological mechanisms, symptom correlations (reasons),
and clinical recommendations for diseases in the MedAssist AI dataset.
"""

DISEASE_KNOWLEDGE_BASE = {
    # --- Viral & Bacterial Infections (including User's Acute Retroviral / Mononucleosis Example) ---
    "Acute HIV Infection": {
        "category": "Retroviral Infection (Acute Retroviral Syndrome)",
        "cause": "Acute infection with the Human Immunodeficiency Virus (HIV-1/HIV-2), a retrovirus targeting CD4+ T helper lymphocytes, dendritic cells, and macrophages.",
        "symptom_hallmarks": ["Fever and Chills", "Fatigue and Weakness", "Sore Throat", "Headache", "Muscle and Joint Aches", "Skin Rash", "Mouth Ulcers", "Swollen Lymph Nodes", "Night Sweats"],
        "pathophysiology": "Rapid initial burst of viral replication in mucosal and gut-associated lymphoid tissue (GALT), precipitating a profound systemic cytokine surge (interferons, TNF-alpha) and transient acute CD4+ decline.",
        "recommended_action": "Seek immediate medical consultation for 4th-generation HIV-1/2 antigen/antibody combo immunoassay and plasma HIV RNA viral load testing. Early initiation of Antiretroviral Therapy (ART) significantly preserves immune function.",
        "urgency": "Urgent Medical Evaluation Required"
    },
    "Infectious Mononucleosis": {
        "category": "Acute Viral Infection (Epstein-Barr Virus)",
        "cause": "Primary viral infection predominantly caused by Epstein-Barr Virus (EBV, Human Herpesvirus 4), transmitted via oropharyngeal secretions ('kissing disease').",
        "symptom_hallmarks": ["Fever and Chills", "Profound Fatigue", "Sore Throat (Exudative Pharyngitis)", "Swollen Lymph Nodes (Cervical)", "Headache", "Muscle Aches"],
        "pathophysiology": "EBV infects naive B lymphocytes in nasopharyngeal lymphoepithelium, eliciting massive polyclonal proliferation of reactive CD8+ cytotoxic T lymphocytes (atypical Downey cells), causing prominent lymphadenopathy and splenomegaly.",
        "recommended_action": "Consult a physician for heterophile antibody test (Monospot) and complete blood count (CBC) with differential. Strict avoidance of contact sports for 3 to 4 weeks to prevent splenic rupture.",
        "urgency": "Moderate to High"
    },
    "Other Viral or Bacterial Infections": {
        "category": "Systemic Viral or Bacterial Infection",
        "cause": "Acute systemic infectious syndromes caused by common viral agents (Cytomegalovirus [CMV], Adenovirus, Enterovirus, Parvovirus B19) or early bacterial bacteremia.",
        "symptom_hallmarks": ["Fever and Chills", "Fatigue and Weakness", "Headache", "Muscle and Joint Aches", "Sore Throat", "Skin Rash"],
        "pathophysiology": "Systemic pathogen recognition by toll-like receptors (TLRs) initiates endogenous pyrogenic cytokine release (IL-1, IL-6, TNF-alpha), causing systemic febrile reaction and muscle catabolism.",
        "recommended_action": "Clinical evaluation by a primary care physician, supportive hydration, antipyretics, and targeted diagnostic serology / cultures if symptoms persist past 7 days.",
        "urgency": "Moderate"
    },
    "Influenza": {
        "category": "Viral Respiratory Infection",
        "cause": "Acute respiratory tract infection caused by Influenza A or B viruses, transmitted via airborne droplets.",
        "symptom_hallmarks": ["Sudden High Fever", "Cough", "Severe Muscle Aches", "Profound Fatigue", "Headache"],
        "pathophysiology": "Lytic viral replication within ciliated columnar epithelial cells leads to denudation of respiratory mucosa and systemic inflammatory mediator release.",
        "recommended_action": "Bed rest, oral fluid replacement, acetaminophen/ibuprofen, and neuraminidase inhibitors (oseltamivir) if within 48 hours of onset.",
        "urgency": "Moderate"
    },
    "Common Cold": {
        "category": "Upper Respiratory Tract Infection",
        "cause": "Mild self-limiting viral infection of the upper respiratory mucosa, primarily rhinoviruses (>50%), coronaviruses, or adenoviruses.",
        "symptom_hallmarks": ["Cough", "Sore Throat", "Mild Fatigue", "Headache"],
        "pathophysiology": "Localized mucosal inflammation mediated by bradykinin and histamine release in nasal and pharyngeal tissues.",
        "recommended_action": "Supportive symptomatic home care, hydration, and saline nasal rinses. Typically resolves within 7 to 10 days.",
        "urgency": "Low"
    },
    "Streptococcal Pharyngitis": {
        "category": "Bacterial Throat Infection (Strep Throat)",
        "cause": "Acute upper respiratory bacterial infection caused by Streptococcus pyogenes (Group A beta-hemolytic Streptococcus, GAS).",
        "symptom_hallmarks": ["Severe Sore Throat", "High Fever", "Swollen Anterior Cervical Lymph Nodes", "Headache", "Absence of Cough"],
        "pathophysiology": "Bacterial adherence and pyrogenic exotoxins induce acute mucosal erythema, follicular tonsillar exudate, and regional lymphadenitis.",
        "recommended_action": "Rapid Strep antigen detection test or throat culture; prescription antibiotic therapy (Penicillin or Amoxicillin) to prevent acute rheumatic fever and peritonsillar abscess.",
        "urgency": "Moderate to High"
    },
    "Pneumonia": {
        "category": "Lower Respiratory Infection",
        "cause": "Infection of pulmonary alveoli and bronchioles caused by bacteria (Streptococcus pneumoniae, Mycoplasma) or respiratory viruses.",
        "symptom_hallmarks": ["High Fever", "Productive Cough", "Difficulty Breathing", "Pleuritic Chest Pain", "Fatigue"],
        "pathophysiology": "Alveolar spaces fill with purulent exudate, inflammatory cells, and fibrin, causing consolidation and impaired oxygen diffusion.",
        "recommended_action": "Prompt medical consultation for chest auscultation, pulse oximetry, and chest radiography. Antibiotic or antiviral therapy.",
        "urgency": "High"
    },
    "Bronchitis": {
        "category": "Bronchial Airway Inflammation",
        "cause": "Acute or subacute inflammation of the bronchial mucous membranes, most commonly following viral upper respiratory infections.",
        "symptom_hallmarks": ["Persistent Cough", "Chest Congestion", "Fatigue", "Mild Fever", "Difficulty Breathing"],
        "pathophysiology": "Epithelial cell sloughing and hyperactive mucociliary response causing bronchial hypersecretion and spasmodic coughing.",
        "recommended_action": "Hydration, bronchodilators if wheezing is present, and clinical follow-up if symptoms persist beyond 2 weeks.",
        "urgency": "Moderate"
    },
    "Asthma": {
        "category": "Chronic Airway Disease",
        "cause": "Chronic inflammatory airway disorder characterized by bronchial hyperresponsiveness and reversible airflow limitation triggered by allergens, cold air, exercise, or viral infections.",
        "symptom_hallmarks": ["Difficulty Breathing", "Wheezing", "Cough", "Chest Tightness"],
        "pathophysiology": "Eosinophil and mast-cell mediated immune cascade causing mucosal edema, mucus hypersecretion, and smooth muscle bronchospasm.",
        "recommended_action": "Consult a pulmonologist for spirometry and inhaled corticosteroid / bronchodilator management. Use rescue inhaler for acute distress.",
        "urgency": "High if acute breathlessness occurs"
    },
    "Chronic Obstructive Pulmonary Disease (COPD)": {
        "category": "Chronic Obstructive Lung Disease",
        "cause": "Progressive, irreversible airflow obstruction caused by long-term toxic inhalation (tobacco smoke, biomass fumes).",
        "symptom_hallmarks": ["Chronic Difficulty Breathing", "Persistent Cough", "Wheezing", "Fatigue"],
        "pathophysiology": "Combination of chronic obstructive bronchitis and emphysematous alveolar wall destruction.",
        "recommended_action": "Smoking cessation, pulmonary function testing (PFT), inhaled dual bronchodilators, and pulmonary rehabilitation.",
        "urgency": "High"
    },
    "COVID-19 / Acute Respiratory Syndrome": {
        "category": "Coronavirus Respiratory Syndrome",
        "cause": "Infection by Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2) targeting ACE2 receptors.",
        "symptom_hallmarks": ["Fever and Chills", "Cough", "Fatigue", "Difficulty Breathing", "Headache", "Muscle Aches"],
        "pathophysiology": "Viral replication in respiratory epithelium triggering immune dysregulation, endothelial injury, and potential microvascular thrombosis.",
        "recommended_action": "Rapid antigen or RT-PCR testing, isolation, pulse oximetry monitoring, and antivirals (Paxlovid) for eligible patients.",
        "urgency": "High if oxygen saturation drops below 95%"
    },
    "Tuberculosis": {
        "category": "Chronic Mycobacterial Infection",
        "cause": "Infection by Mycobacterium tuberculosis transmitted via airborne droplets.",
        "symptom_hallmarks": ["Persistent Cough (>3 weeks)", "Night Sweats", "Unexplained Weight Loss", "Low-Grade Fever", "Fatigue"],
        "pathophysiology": "Granulomatous alveolar inflammation with central caseous necrosis and cavitation.",
        "recommended_action": "Chest X-ray, sputum GeneXpert/AFB smear, and multi-drug antimycobacterial regimen.",
        "urgency": "High"
    },
    "Dengue Fever": {
        "category": "Mosquito-Borne Flavivirus Infection",
        "cause": "Infection with Dengue virus (DENV 1-4) transmitted by Aedes mosquitoes.",
        "symptom_hallmarks": ["High Fever", "Severe Headache", "Retro-orbital Pain", "Severe Muscle/Joint Pain ('Breakbone')", "Skin Rash"],
        "pathophysiology": "Viral infection of dendritic and reticuloendothelial cells inducing high capillary permeability and transient thrombocytopenia.",
        "recommended_action": "Complete blood count (CBC) to monitor platelets and hematocrit; oral rehydration; strictly avoid NSAIDs/Aspirin.",
        "urgency": "High"
    },
    "Malaria": {
        "category": "Parasitic Protozoan Infection",
        "cause": "Infection with Plasmodium parasites (P. falciparum, P. vivax) transmitted by Anopheles mosquitoes.",
        "symptom_hallmarks": ["Paroxysmal High Fever", "Shaking Chills", "Profuse Night Sweats", "Headache", "Fatigue"],
        "pathophysiology": "Cyclic intra-erythrocytic schizogony and red blood cell rupture releasing pyrogenic toxins into the bloodstream.",
        "recommended_action": "Emergency thick and thin blood smear or rapid antigen test; immediate Artemisinin-based Combination Therapy (ACT).",
        "urgency": "Emergency Medical Evaluation"
    },
    "Typhoid Fever": {
        "category": "Enteric Bacterial Infection",
        "cause": "Systemic bacterial infection caused by Salmonella enterica serotype Typhi through contaminated food or water.",
        "symptom_hallmarks": ["Stepladder Fever", "Abdominal Pain", "Headache", "Fatigue", "Loss of Appetite"],
        "pathophysiology": "Bacterial translocation through Peyer's patches with reticuloendothelial multiplication and secondary bacteremia.",
        "recommended_action": "Blood culture, stool culture, and appropriate antibiotic therapy (Ceftriaxone or Azithromycin).",
        "urgency": "High"
    },
    "Gastroenteritis": {
        "category": "Gastrointestinal Infection",
        "cause": "Acute inflammation of gastric and intestinal mucosa caused by viral (Norovirus, Rotavirus) or bacterial pathogens.",
        "symptom_hallmarks": ["Nausea and Vomiting", "Watery Diarrhea", "Abdominal Cramps", "Low Fever", "Fatigue"],
        "pathophysiology": "Enterotoxin-mediated mucosal secretagogue stimulation or direct enterocyte villous blunting.",
        "recommended_action": "Oral rehydration solution (ORS), electrolyte monitoring, and light diet. Seek care if unable to hold liquids.",
        "urgency": "Moderate"
    },
    "Appendicitis": {
        "category": "Acute Surgical Abdomen",
        "cause": "Obstruction of the appendiceal lumen by fecalith, lymphoid hyperplasia, or foreign body, leading to bacterial superinfection.",
        "symptom_hallmarks": ["Severe Right Lower Quadrant Abdominal Pain", "Nausea and Vomiting", "Fever", "Loss of Appetite"],
        "pathophysiology": "Intraluminal distension, ischemic transmural necrosis, and potential perforation.",
        "recommended_action": "EMERGENT surgical evaluation and abdominal ultrasound / CT scan. NPO (do not eat or drink).",
        "urgency": "Surgical Emergency"
    },
    "Crohn's Disease": {
        "category": "Inflammatory Bowel Disease",
        "cause": "Chronic transmural inflammatory condition of the GI tract driven by genetic susceptibility, immune dysregulation, and microbiome alterations.",
        "symptom_hallmarks": ["Chronic Abdominal Pain", "Diarrhea", "Weight Loss", "Fatigue", "Mouth Ulcers"],
        "pathophysiology": "Dysregulated Th1/Th17 immune response resulting in transmural skip lesions and granulomatous inflammation.",
        "recommended_action": "Gastroenterologist consultation, colonoscopy with biopsy, and biologic / immunosuppressive therapy.",
        "urgency": "High"
    },
    "Ulcerative Colitis": {
        "category": "Inflammatory Bowel Disease",
        "cause": "Chronic mucosal inflammatory disease restricted to the colon and rectum.",
        "symptom_hallmarks": ["Bloody Diarrhea", "Abdominal Cramping", "Tenesmus", "Fatigue", "Weight Loss"],
        "pathophysiology": "Superficial continuous mucosal ulcerations and crypt abscesses.",
        "recommended_action": "Colonoscopy with histology and initiation of 5-ASA (mesalamine) or immunomodulator therapy.",
        "urgency": "High"
    },
    "Urinary Tract Infection (UTI)": {
        "category": "Urological Bacterial Infection",
        "cause": "Ascending bacterial colonization of the bladder and urethra, predominantly uropathogenic Escherichia coli.",
        "symptom_hallmarks": ["Painful Urination (Dysuria)", "Urinary Frequency & Urgency", "Low Fever", "Pelvic Discomfort"],
        "pathophysiology": "Bacterial adhesins bind uroepithelial receptors, provoking acute mucosal inflammation and leukocyturia.",
        "recommended_action": "Urinalysis with microscopy and targeted oral antibiotic treatment.",
        "urgency": "Moderate"
    },
    "Measles": {
        "category": "Viral Exanthematous Disease",
        "cause": "Infection with the Measles morbillivirus transmitted via airborne droplets.",
        "symptom_hallmarks": ["High Fever", "Maculopapular Skin Rash", "Cough", "Mouth Ulcers (Koplik spots)", "Sore Throat"],
        "pathophysiology": "Viremic dissemination to endothelial and epithelial cells with delayed-type hypersensitivity rash.",
        "recommended_action": "Immediate medical isolation, supportive care, and Vitamin A supplementation under clinical supervision.",
        "urgency": "High"
    },
    "Chickenpox": {
        "category": "Herpesvirus Exanthematous Disease",
        "cause": "Primary infection with Varicella Zoster Virus (VZV).",
        "symptom_hallmarks": ["Pruritic Vesicular Skin Rash", "Fever", "Fatigue", "Loss of Appetite"],
        "pathophysiology": "Replication in respiratory lymphoid tissue followed by viremia and vesicular cutaneous eruption.",
        "recommended_action": "Antihistamines, calamine lotion, paracetamol (avoid aspirin in children), and antiviral therapy if high-risk.",
        "urgency": "Moderate"
    },
    "Lyme Disease": {
        "category": "Tick-Borne Spirochetal Infection",
        "cause": "Infection with Borrelia burgdorferi transmitted by Ixodes ticks.",
        "symptom_hallmarks": ["Erythema Migrans (Bull's Eye Rash)", "Fever and Chills", "Fatigue", "Headache", "Joint Aches"],
        "pathophysiology": "Spirochete dissemination through dermal tissues and blood, provoking intense immunogenic joint and nerve inflammation.",
        "recommended_action": "Clinical evaluation for Doxycycline antibiotic therapy and tick-borne serology.",
        "urgency": "Moderate to High"
    },
    "Systemic Lupus Erythematosus (SLE)": {
        "category": "Systemic Autoimmune Disease",
        "cause": "Complex autoimmune disease characterized by immune complex deposition and autoantibodies against nuclear antigens (ANA, anti-dsDNA).",
        "symptom_hallmarks": ["Malar Butterfly Rash", "Joint Pain & Swelling", "Mouth Ulcers", "Fever", "Profound Fatigue", "Chest Pain"],
        "pathophysiology": "Defective clearance of apoptotic cells triggers immune complex formation and widespread microvascular inflammation.",
        "recommended_action": "Rheumatology referral; autoimmune serology (ANA, anti-dsDNA, complement C3/C4); hydroxychloroquine therapy.",
        "urgency": "High"
    },
    "Rheumatoid Arthritis": {
        "category": "Autoimmune Joint Disease",
        "cause": "Chronic autoimmune inflammatory polyarthritis targeting synovial joints.",
        "symptom_hallmarks": ["Joint Swelling & Stiffness", "Morning Stiffness > 1 hr", "Fatigue", "Muscle Aches"],
        "pathophysiology": "Synovial hyperplasia and pannus formation causing cartilage erosion and subchondral bone remodeling.",
        "recommended_action": "Rheumatologist evaluation for RF and anti-CCP antibodies; early DMARD therapy.",
        "urgency": "Moderate"
    },
    "Migraine": {
        "category": "Neurological Neurovascular Disorder",
        "cause": "Neurovascular disorder involving cortical spreading depression and trigeminovascular sensitization.",
        "symptom_hallmarks": ["Unilateral Throbbing Headache", "Nausea and Vomiting", "Photophobia", "Dizziness", "Fatigue"],
        "pathophysiology": "Trigeminal nerve activation with calcitonin gene-related peptide (CGRP) release causing meningeal vasodilation.",
        "recommended_action": "Neurologist consultation, trigger identification, and triptan / CGRP antagonist management.",
        "urgency": "Moderate"
    },
    "Hypertension": {
        "category": "Cardiovascular Disorder",
        "cause": "Persistent elevation of systemic arterial blood pressure due to vascular resistance and autonomic dysregulation.",
        "symptom_hallmarks": ["Headache", "Dizziness", "Fatigue", "Often Asymptomatic ('Silent')"],
        "pathophysiology": "Increased afterload, vascular remodeling, and accelerated target-organ atherosclerosis.",
        "recommended_action": "Comprehensive cardiovascular risk assessment, lifestyle changes, and antihypertensive therapy.",
        "urgency": "Moderate"
    },
    "Coronary Artery Disease": {
        "category": "Ischemic Heart Disease",
        "cause": "Coronary atherosclerotic plaque buildup reducing myocardial perfusion.",
        "symptom_hallmarks": ["Chest Pain / Angina", "Difficulty Breathing", "Fatigue", "Dizziness"],
        "pathophysiology": "Fixed luminal stenosis or plaque disruption precipitating subendocardial ischemia.",
        "recommended_action": "Urgent cardiology evaluation, 12-lead ECG, cardiac biomarkers, and statin/antiplatelet therapy.",
        "urgency": "High"
    },
    "Stroke": {
        "category": "Cerebrovascular Emergency",
        "cause": "Acute disruption of cerebral blood supply (ischemic thrombosis or hemorrhage).",
        "symptom_hallmarks": ["Sudden Severe Headache", "Dizziness", "Facial Droop", "Unilateral Weakness", "Speech Difficulty"],
        "pathophysiology": "Focal cerebral ischemia producing rapid neuronal depolarization and ischemic penumbra necrosis.",
        "recommended_action": "EMERGENCY: Immediate emergency hospitalization (FAST protocol) for CT/MRI and reperfusion therapy.",
        "urgency": "Medical Emergency"
    },
    "Diabetes Mellitus": {
        "category": "Metabolic & Endocrine Disorder",
        "cause": "Impaired insulin secretion and/or peripheral insulin resistance causing chronic hyperglycemia.",
        "symptom_hallmarks": ["Fatigue and Weakness", "Frequent Urination", "Excessive Thirst", "Unexplained Weight Loss"],
        "pathophysiology": "Glucose toxicity, advanced glycation end products, and microvascular / macrovascular complications.",
        "recommended_action": "Fasting blood glucose, HbA1c testing, diabetic education, and pharmacological therapy.",
        "urgency": "Moderate"
    },
    "Osteoporosis": {
        "category": "Metabolic Bone Disorder",
        "cause": "Imbalance in bone remodeling where osteoclastic resorption exceeds osteoblastic formation.",
        "symptom_hallmarks": ["Bone Fragility", "Back Pain", "Loss of Height", "Muscle & Joint Aches"],
        "pathophysiology": "Deterioration of bone microarchitecture with decreased bone mineral density.",
        "recommended_action": "DEXA bone mineral density scan, Vitamin D / calcium supplementation, and bisphosphonate therapy.",
        "urgency": "Moderate"
    },
    "Sinusitis": {
        "category": "Upper Respiratory Sinus Infection",
        "cause": "Inflammation and mucosal edema of paranasal sinuses causing ostial blockage.",
        "symptom_hallmarks": ["Facial Pressure", "Headache", "Cough", "Sore Throat", "Fever"],
        "pathophysiology": "Impaired mucociliary clearance leading to mucus stasis and secondary microbial proliferation.",
        "recommended_action": "Nasal saline irrigation, topical corticosteroid spray, and hydration.",
        "urgency": "Moderate"
    },
    "Allergic Rhinitis": {
        "category": "Allergic Atopic Condition",
        "cause": "IgE-mediated hypersensitivity reaction to airborne allergens (pollen, dust mites, pet dander).",
        "symptom_hallmarks": ["Sneezing", "Nasal Congestion", "Itching", "Cough", "Headache", "Fatigue"],
        "pathophysiology": "Allergen cross-linking on sensitized mast cells triggers immediate histamine and leukotriene release.",
        "recommended_action": "Non-sedating oral antihistamines, allergen avoidance, and intranasal corticosteroids.",
        "urgency": "Low"
    }
}


def get_disease_knowledge(disease_name: str) -> dict:
    """Retrieve structured medical knowledge for a given disease name."""
    if disease_name in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[disease_name]

    # Fuzzy/case-insensitive match
    norm_target = disease_name.lower().strip()
    for name, data in DISEASE_KNOWLEDGE_BASE.items():
        if name.lower() in norm_target or norm_target in name.lower():
            return data

    return {
        "category": "Clinical Medical Condition",
        "cause": f"{disease_name} is an identified clinical syndrome involving multifactorial pathophysiology, environmental triggers, and individual biological susceptibility.",
        "symptom_hallmarks": ["Characteristic presentation across involved organ systems"],
        "pathophysiology": "Cellular and functional tissue adaptations resulting from underlying infectious, metabolic, or degenerative stressors.",
        "recommended_action": "Consult a qualified medical specialist for formal in-person examination, laboratory analysis, and customized management.",
        "urgency": "Moderate"
    }


def generate_clinical_explanation(disease: str, patient_data: dict, model_score: float, rank: int = 1) -> dict:
    """Synthesizes a personalized medical explanation including Reason and Cause."""
    knowledge = get_disease_knowledge(disease)

    # Format present symptoms
    raw_symptoms = patient_data.get("symptoms", [])
    if isinstance(raw_symptoms, str):
        try:
            import json
            raw_symptoms = json.loads(raw_symptoms)
        except Exception:
            raw_symptoms = [raw_symptoms]

    symptom_display = [s.replace("_", " ").title() for s in raw_symptoms]
    symptom_str = ", ".join(symptom_display) if symptom_display else "non-specific general symptoms"

    age = patient_data.get("Age") or patient_data.get("age", 0)
    bp = patient_data.get("Blood Pressure") or patient_data.get("blood_pressure", "Normal")
    chol = patient_data.get("Cholesterol Level") or patient_data.get("cholesterol_level", "Normal")
    duration = patient_data.get("duration_days", 1)
    patient_name = patient_data.get("patient_name") or "The patient"

    # Clinical Reason Formulation
    reason_parts = [
        f"The prediction of {disease} is substantiated by the constellation of reported clinical manifestations: [{symptom_str}]."
    ]

    if "HIV" in disease or "Mononucleosis" in disease or "Viral" in disease:
        reason_parts.append(
            "This combination of systemic fever, lymphadenopathy, pharyngitis, skin/mucosal findings, and constitutional fatigue is a hallmark presentation in the Human Symptoms-Disease Network for acute viral syndromes."
        )

    if bp == "High" and ("Cardiovascular" in knowledge["category"] or "Hypertension" in disease or "Stroke" in disease):
        reason_parts.append(f"Elevated blood pressure ({bp}) serves as a compounding vascular hemodynamic risk factor.")

    if duration >= 7:
        reason_parts.append(f"The symptom duration of {duration} days indicates subacute progression requiring timely diagnostic confirmation.")

    reason_text = " ".join(reason_parts)

    # Calibrated confidence tier
    if model_score >= 0.65:
        confidence_tier = "High Confidence"
        confidence_desc = f"Strong symptom-pattern alignment ({model_score:.1%})"
    elif model_score >= 0.30:
        confidence_tier = "Moderate Confidence"
        confidence_desc = f"Moderate clinical correlation ({model_score:.1%})"
    else:
        confidence_tier = "Screening Consideration"
        confidence_desc = f"Differential consideration ({model_score:.1%})"

    return {
        "disease": disease,
        "rank": rank,
        "probability": round(float(model_score), 4),
        "probability_percent": f"{model_score * 100:.1f}%",
        "confidence_tier": confidence_tier,
        "confidence_description": confidence_desc,
        "category": knowledge["category"],
        "cause": knowledge["cause"],
        "pathophysiology": knowledge["pathophysiology"],
        "clinical_reason": reason_text,
        "recommended_action": knowledge["recommended_action"],
        "urgency": knowledge["urgency"],
        "matched_symptoms": symptom_display
    }
