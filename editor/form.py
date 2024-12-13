from django import forms

class EditorBox(forms.Form):
    python_code = forms.CharField(widget=forms.Textarea(attrs={'rows':10,'cols':30,'class':"border-secondary w-100",'id':'code-box','spellcheck':'false'}))

class RequestProblem(forms.Form):
    request_button = forms.CharField(widget=forms.HiddenInput(), initial='submit')

class ChatBox(forms.Form):
    chat_box = forms.CharField(widget=forms.TextInput(attrs={'class':"mb-1 w-100"}))

class LogOut(forms.Form):
    logout_button = forms.CharField(widget=forms.HiddenInput(), initial='submit')

class ExperienceForm(forms.Form):
    experience = forms.CharField(widget=forms.TextInput(attrs={'class':'w-100'}))