from django import forms
from scrap.models import City, ProgrammingLanguage


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all())
    programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all())