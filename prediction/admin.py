from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'sex', 'prediction_result', 'created_at']
    list_filter = ['prediction_result', 'sex', 'created_at']
    search_fields = ['id']