from django import forms

class EditorBox(forms.Form):
    python_code = forms.CharField(widget=forms.Textarea(attrs={'rows':10,'cols':30,'class':"border-secondary w-100"}))