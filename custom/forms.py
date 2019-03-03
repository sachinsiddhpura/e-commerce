from django import forms

from .models import Custom


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = '__all__'
