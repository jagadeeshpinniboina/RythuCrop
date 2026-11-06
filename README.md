# RythuCrop (రైతుక్రాప్) 🌱🌾

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**RythuCrop** is an enterprise-grade AI agritech SaaS platform engineered specifically for Indian agriculture. It equips farmers, agronomists, and agricultural stakeholders with real-time agronomic intelligence, AI-driven crop suitability rankings, pre-harvest seasonal yield forecasting, end-to-end farm planning economics, and actionable smart advisory across **10 Indic languages**.

---

## 🚀 Key Modules & Architecture

### 1. 📊 Precision Farm Planning & Economics
- **Dynamic Agronomic Cost Modeling:** Calculates seed requirements, basal & top-dressing fertilizer costs, labor, irrigation, and harvest outlays per acre/hectare.
- **Yield & Net Revenue Projection:** Integrates historical APMC mandi pricing and MSP benchmarks to forecast gross revenue, operational expenses, and net profit margins.
- **Investment Risk Analysis:** Categorizes farm ventures into Low, Moderate, or High-risk profiles based on capital intensity and climate resilience.

### 2. 🤖 AI Crop Recommendation Engine
- **Multi-Factor Agronomic Scoring:** Analyzes soil chemistry (Nitrogen, Phosphorus, Potassium, Soil pH) combined with atmospheric conditions (Temperature, Relative Humidity, Rainfall).
- **Ensemble Machine Learning:** Employs an optimized Random Forest classifier delivering **sub-100ms inferences** with in-memory caching.
- **Top-3 Ranked Recommendations:** Delivers optimal crop recommendations with probability match percentages, soil suitability ratings, and agronomic justification cards.

### 3. 📈 Seasonal Yield Forecasting
- **Pre-Harvest Productivity Estimation:** Predicts seasonal yield (Quintals/Acre and Tonnes/Hectare) based on geographic district, crop variety, seasonal window (Kharif, Rabi, Summer, Whole Year), and crop acreage.
- **Full Seasonal Yield Matrix:** Generates an automated cross-season productivity comparison table across all 4 agro-climatic seasons.
- **Target Leakage Prevention:** Built on retrained, production-hardened models with verified cross-validation to prevent feature leakage.

### 4. 💡 Actionable Smart Advisory
- **Focused Cultivation Guides:** Filterable guidance cards covering:
  1. *Step-by-Step Crop Care:* Land preparation, seed treatment, irrigation scheduling, and intercultural operations.
  2. *Fertilizer Schedules:* Tailored N-P-K splits, micronutrient management, and organic compost application timelines.
  3. *Pest & Disease Mitigation:* Identification keys, economic threshold levels (ETL), and integrated pest management (IPM) protocols.

---

## 🌐 10-Language Indic Translation Engine (Zero-Leakage)

RythuCrop features a high-performance, zero-leakage internationalization architecture providing native language support across 10 official languages:

| Language | Code | Script |
| :--- | :---: | :--- |
| **English** | `en` | Latin |
| **Telugu (తెలుగు)** | `te` | Telugu |
| **Hindi (हिन्दी)** | `hi` | Devanagari |
| **Tamil (தமிழ்)** | `ta` | Tamil |
| **Kannada (ಕನ್ನಡ)** | `kn` | Kannada |
| **Malayalam (മലയാളം)** | `ml` | Malayalam |
| **Marathi (मराठी)** | `mr` | Devanagari |
| **Bengali (বাংলা)** | `bn` | Bengali |
| **Gujarati (ગુજરાતી)** | `gu` | Gujarati |
| **Odia (ଓଡ଼ିଆ)** | `od` | Odia |

Dynamic client-side translation caches and server-side fallback dictionaries ensure instant switching without page reloads or raw English leakage in dynamic model outputs.

---

## 🔒 Security & Authentication Architecture

- **Session & Email-Based Authentication Gating:** All 4 analytical endpoints require verified user sessions. Unauthenticated access triggers immediate, friendly authentication modals.
- **Dual-Channel OTP Dispatch:** Production Twilio WhatsApp sandbox integration with automated SMS/terminal fallback for local development and testing.
- **Zero-Trust Input Validation:** Strict bounds checking on N-P-K inputs, pH levels (3.5 - 9.0), rainfall, temperature, and area parameters.
- **Hardened Error Handling:** Defensive route handlers returning structured JSON error payloads, preventing 500 tracebacks.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, Flask, Werkzeug, Jinja2
- **Machine Learning:** Scikit-learn, NumPy, Pandas, Joblib
- **Frontend:** Vanilla ES6+ JavaScript, HTML5, Tailwind CSS (utility styling with emerald/agritech theme)
- **Deployment & Concurrency:** Multi-threaded WSGI runtime (`run.py`), defensive JSON parsers, GCM integration
- **Testing:** Pytest, custom end-to-end integration test suites

---

## 📁 Repository Structure

```text
├── app/
│   ├── data/                 # Dynamic crop parameters, pricing & Indic translations
│   ├── routes/               # Modular Flask blueprints (auth, prediction, advisory, planning)
│   ├── static/
│   │   ├── js/               # Modular ES6 client controllers (advisory, farm_planning, yield, recommendation)
│   │   ├── images/           # High-resolution agronomic visual assets
│   │   └── style.css         # Tailwind utility extensions & responsive media queries
│   └── templates/
│       └── index.html        # Single-page application shell with data-i18n attributes
├── data/                     # Cleaned agricultural datasets (soil, climate, APMC mandi records)
├── ml/
│   ├── saved_models/         # Serialized Scikit-learn models (crop recommendation & yield)
│   └── train_*.py            # Reproducible model training pipelines
├── tests/                    # Automated regression and API test suites
├── config.py                 # Multi-environment configuration loader
├── requirements.txt          # Production dependencies
├── run.py                    # Multi-threaded server launcher
└── README.md                 # Project documentation
```

---

## ⚡ Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jagadeeshpinniboina/RythuCrop.git
cd RythuCrop
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and set your credentials:
```bash
cp .env.example .env
```
*(Optional for local testing: Twilio credentials can be omitted to use terminal-based OTP logging).*

### 5. Launch Application
```bash
python run.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🧪 Running the Test Suite

Run the full automated test suite covering authentication gating, model inference, translation completeness, and validation boundaries:
```bash
pytest tests/ -v
# Or run the comprehensive master verification:
python tests/test_master_suite.py
python tests/test_all_features.py
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
