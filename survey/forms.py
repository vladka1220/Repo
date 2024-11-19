from django.forms import ModelForm
from .models import Survey, Question, Answer, Choice


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = 'id'
