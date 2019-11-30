from django import forms

class VerseForm(forms.Form):
    message = forms.TextField(max_length=300, widget=forms.Textarea(), help_text='Write your verse here')

    cleaned_data = super(VerseForm, self).clean()
    message = cleaned_data.get('message')
