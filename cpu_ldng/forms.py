from django.forms import ModelForm
from .models import ModelStartStop

class Form_StartStop(ModelForm):
    class Meta:
        model = ModelStartStop
        fields = ['Start_Model', 'Stop_Model', 'Reset_Model', 'Create_Fig_Model', 'Send_Fig_Model']