from django import forms
from .models import Presentation

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['name', 'slides']
        labels = {
            'name': 'Название презентации',
            'slides': 'Слайды',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slides': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slides'].required = False
