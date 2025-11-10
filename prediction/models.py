
from django.db import models

class Prediction(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    CHEST_PAIN_CHOICES = [
        ('ATA', 'ATA'), ('NAP', 'NAP'), 
        ('TA', 'TA'), ('ASY', 'ASY')
    ]
    RESTING_ECG_CHOICES = [
        ('Normal', 'Normal'), ('ST', 'ST'), ('LVH', 'LVH')
    ]
    EXERCISE_ANGINA_CHOICES = [('Y', 'Yes'), ('N', 'No')]
    ST_SLOPE_CHOICES = [
        ('Up', 'Up'), ('Flat', 'Flat'), ('Down', 'Down')
    ]
    
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    chest_pain_type = models.CharField(max_length=3, choices=CHEST_PAIN_CHOICES)
    resting_bp = models.IntegerField()
    cholesterol = models.IntegerField()
    fasting_bs = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])
    resting_ecg = models.CharField(max_length=10, choices=RESTING_ECG_CHOICES)
    max_hr = models.IntegerField()
    exercise_angina = models.CharField(max_length=1, choices=EXERCISE_ANGINA_CHOICES)
    oldpeak = models.FloatField()
    st_slope = models.CharField(max_length=4, choices=ST_SLOPE_CHOICES)
    prediction_result = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - {'High Risk' if self.prediction_result == 1 else 'Low Risk'}"

    def get_risk_level(self):
        return "High Risk" if self.prediction_result == 1 else "Low Risk"