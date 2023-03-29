from django import forms
from . models import Mark


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'mark': forms.TextInput(attrs={'class': 'form-control'}),

            # 'num_of_products': forms.TextInput(attrs={'class': 'form-control'}),
        }
