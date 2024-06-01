# forms.py
from djongo import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
