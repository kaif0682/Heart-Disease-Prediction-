# Heart Disease Prediction

A Django web application that estimates a user's heart disease risk from selected health measurements using a pre-trained K-nearest neighbors (KNN) classifier. The app displays the result and saves submitted measurements and predictions to a local SQLite database.

> **Medical disclaimer:** This project is for educational and informational purposes only. It is not a medical device and must not be used to diagnose, treat, or rule out a medical condition. Consult a qualified healthcare professional for medical advice.

## Overview

The application presents a web form for entering demographic, blood, and heart-related measurements. On submission, Django prepares the input features in the order expected by the saved training artifacts, scales them, and asks the KNN model for a binary prediction and its class-1 probability. The result is returned to the page and saved as a `Prediction` record.

The model training workflow is provided separately in `Notebook/HeartdiseaseFinal.ipynb`, with the source dataset in `Data/heart.csv`. The app loads the model artifacts at startup; it does not train the model during a request.

## Features

- Browser-based form for heart-related measurements.
- KNN model inference using a saved scaler and expected feature columns.
- Binary high-risk/low-risk result with a model probability score.
- Detailed result page for a saved prediction.
- SQLite persistence of submitted values and prediction results.
- Health endpoint indicating whether the model artifacts loaded.

## Technology

- Python
- Django (settings generated with Django 5.2.1)
- pandas
- scikit-learn
- joblib
- SQLite
- HTML, CSS, and browser JavaScript
- Jupyter Notebook for the model-training workflow

There is no dependency manifest in the project, so exact versions for the runtime libraries are not pinned. The installed scikit-learn version must be compatible with the serialized model and scaler.

The notebook also imports NumPy and Matplotlib; install those, plus Jupyter, if you plan to run the training notebook.

## Project structure

```text
Heart Disease Prediction/
├── Data/
│   └── heart.csv
├── Notebook/
│   └── HeartdiseaseFinal.ipynb
├── README.md
└── heart_disease_app/
    ├── .gitignore
    ├── KNN_heart.pkl
    ├── columns.pkl
    ├── scaler.pkl
    ├── db.sqlite3                 # local SQLite database; updated by Django
    ├── manage.py
    ├── heart_disease_app/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── prediction/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations/
        │   ├── __init__.py
        │   └── 0001_initial.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        └── templates/prediction/
            ├── base.html
            ├── index.html
            └── result.html
```

`manage.py` is the Django command-line entry point. The app expects all three `.pkl` model artifacts to be in the same directory as `manage.py`.

## Prerequisites

- Python installed and available as `python` (or use the platform-specific Python launcher).
- pip.
- The provided model artifacts: `KNN_heart.pkl`, `scaler.pkl`, and `columns.pkl`.

## Local setup

Run these commands from the repository root. They create and activate a virtual environment, install the runtime packages imported by the app, and apply the database migrations.

### Windows PowerShell

```powershell
cd .\heart_disease_app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install Django pandas scikit-learn joblib
python manage.py migrate
```

If PowerShell does not allow activation scripts, run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install Django pandas scikit-learn joblib
.\.venv\Scripts\python.exe manage.py migrate
```

### macOS or Linux

```bash
cd heart_disease_app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install Django pandas scikit-learn joblib
python manage.py migrate
```

No application environment variables are read by the current code. Django uses SQLite at `heart_disease_app/db.sqlite3` (the directory containing `manage.py`).

## Run the application

From the `heart_disease_app` directory, with the virtual environment activated:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser. The development server is for local development only.

## Usage

1. Open the home page and enter the requested measurements.
2. Submit the form to receive a high-risk or low-risk classification and probability score.
3. Select **View Detailed Report** to see the submitted values and the saved prediction record.

Input values and categorical options are defined in the form in `prediction/templates/prediction/index.html`. The backend expects the corresponding form field names and category values.

## HTTP endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Displays the risk assessment form and model availability status. |
| `POST` | `/predict/` | Accepts the form fields, returns JSON with `prediction`, `risk_probability`, and `prediction_id`, and stores the prediction. |
| `GET` | `/result/<prediction_id>/` | Displays the detailed report for a saved prediction. |
| `GET` | `/health/` | Returns JSON with model load status, expected input-column count, and model type. |
| `GET` | `/admin/` | Django administration site. |

The prediction request fields are `age`, `sex`, `chest_pain`, `resting_bp`, `cholesterol`, `fasting_bs`, `resting_ecg`, `max_hr`, `exercise_angina`, `oldpeak`, and `st_slope`. Successful prediction responses contain:

```json
{
  "prediction": 0,
  "risk_probability": 12.34,
  "prediction_id": 1
}
```

The numeric values above are an example of the response shape, not an actual model result.

## Model and data

The model artifacts are loaded by `prediction/views.py` from the app directory:

- `KNN_heart.pkl` — trained classifier.
- `scaler.pkl` — feature scaler fitted during training.
- `columns.pkl` — expected feature names and ordering.

If an artifact is absent or cannot be loaded, the home page reports model unavailability and predictions cannot be made. The training notebook documents a workflow using scikit-learn's `KNeighborsClassifier` and `StandardScaler`; review it before retraining or replacing the artifacts.


## Production considerations

The checked-in Django settings enable debug mode and contain a development secret key. Before deploying, configure a private secret key, disable debug mode, set allowed hosts, and follow Django's deployment checklist. Do not use the bundled development settings for a public production deployment.
