from django.shortcuts import render
from django.http import JsonResponse
from .models import Prediction
import joblib
import pandas as pd
import os
from django.conf import settings

# Global variables for ML model
model = None
scaler = None
expected_columns = None
model_loaded = False

# Load ML model when the app starts
def load_ml_model():
    global model, scaler, expected_columns, model_loaded
    try:
        # Make sure the .pkl files are in the same directory as manage.py
        base_dir = settings.BASE_DIR
        
        model_path = os.path.join(base_dir, 'KNN_heart.pkl')
        scaler_path = os.path.join(base_dir, 'scaler.pkl')
        columns_path = os.path.join(base_dir, 'columns.pkl')
        
        if all(os.path.exists(path) for path in [model_path, scaler_path, columns_path]):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            expected_columns = joblib.load(columns_path)
            model_loaded = True
            print("✅ ML model loaded successfully!")
        else:
            print("❌ ML model files not found. Please check file paths.")
            model_loaded = False
    except Exception as e:
        print(f"❌ Error loading ML model: {e}")
        model_loaded = False

# Load model when module is imported
load_ml_model()

def index(request):
    context = {
        'model_loaded': model_loaded
    }
    return render(request, 'prediction/index.html', context)

def predict(request):
    if request.method == 'POST':
        try:
            # Check if model is loaded
            if not model_loaded:
                return JsonResponse({'error': 'Prediction model is not available. Please check if model files are present.'}, status=500)

            # Get form data
            age = int(request.POST.get('age'))
            sex = request.POST.get('sex')
            chest_pain = request.POST.get('chest_pain')
            resting_bp = int(request.POST.get('resting_bp'))
            cholesterol = int(request.POST.get('cholesterol'))
            fasting_bs = int(request.POST.get('fasting_bs'))
            resting_ecg = request.POST.get('resting_ecg')
            max_hr = int(request.POST.get('max_hr'))
            exercise_angina = request.POST.get('exercise_angina')
            oldpeak = float(request.POST.get('oldpeak'))
            st_slope = request.POST.get('st_slope')

            # Create input dictionary with one-hot encoding
            raw_input = {
                'Age': age,
                'RestingBP': resting_bp,
                'Cholesterol': cholesterol,
                'FastingBS': fasting_bs,
                'MaxHR': max_hr,
                'Oldpeak': oldpeak,
                f'Sex_{sex}': 1,
                f'ChestPainType_{chest_pain}': 1,
                f'RestingECG_{resting_ecg}': 1,
                f'ExerciseAngina_{exercise_angina}': 1,
                f'ST_Slope_{st_slope}': 1
            }

            # Create input dataframe
            input_df = pd.DataFrame([raw_input])

            # Fill in missing columns with 0s
            for col in expected_columns:
                if col not in input_df.columns:
                    input_df[col] = 0

            # Reorder columns to match training data
            input_df = input_df[expected_columns]

            # Scale the input
            scaled_input = scaler.transform(input_df)

            # Make prediction
            prediction_result = model.predict(scaled_input)[0]
            prediction_proba = model.predict_proba(scaled_input)[0]

            # Get probability scores
            risk_probability = float(prediction_proba[1])  # Probability of high risk

            # Save prediction to database
            prediction = Prediction(
                age=age,
                sex=sex,
                chest_pain_type=chest_pain,
                resting_bp=resting_bp,
                cholesterol=cholesterol,
                fasting_bs=fasting_bs,
                resting_ecg=resting_ecg,
                max_hr=max_hr,
                exercise_angina=exercise_angina,
                oldpeak=oldpeak,
                st_slope=st_slope,
                prediction_result=prediction_result
            )
            prediction.save()

            # Return JSON response for AJAX call
            return JsonResponse({
                'prediction': int(prediction_result),
                'risk_probability': round(risk_probability * 100, 2),
                'prediction_id': prediction.id
            })

        except Exception as e:
            print(f"Prediction error: {e}")
            return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def result(request, prediction_id):
    try:
        prediction = Prediction.objects.get(id=prediction_id)
        context = {
            'prediction': prediction
        }
        return render(request, 'prediction/result.html', context)
    except Prediction.DoesNotExist:
        return render(request, 'prediction/error.html', {'message': 'Prediction not found'})

def health_check(request):
    """Check if ML model is loaded properly"""
    return JsonResponse({
        'model_loaded': model_loaded,
        'expected_columns_count': len(expected_columns) if model_loaded else 0,
        'model_type': type(model).__name__ if model_loaded else 'None'
    })