from django import forms
from .models import Genre

class VerseForm(forms.Form):
    story = forms.CharField(max_length=300, widget=forms.Textarea({'rows':3, 'cols':50}))
    def clean(self):
        cleaned_data = super(VerseForm, self).clean()
        story = cleaned_data.get('story')
        if not story:
            raise forms.ValidationError('Write a story!')


class NewVerseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NewVerseForm, self).__init__(*args, **kwargs)
        genres = Genre.objects.values_list('name', flat=True)
        self.fields['genre'] = forms.CharField(widget=forms.SelectMultiple(choices=tuple((g,g.capitalize) for g in genres)))

    story = forms.CharField(max_length=300, widget=forms.Textarea({'rows':3, 'cols':50}))
    def clean(self):
        cleaned_data = super(NewVerseForm, self).clean()
        story = cleaned_data.get('story')
        genre = cleaned_data.get('genre')
        if not story:
            raise forms.ValidationError('Write a story!')


class AddGenreForm(forms.Form):
    name = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(AddGenreForm, self).clean()
        name = cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Write a name!')
