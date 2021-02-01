from django import forms
from scrap.models import City, ProgrammingLanguage, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name="slug",
                                  required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  label='Город')
    programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all(),
                                                  to_field_name="slug",
                                                  required=False,
                                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                                  label='Специальность')


class CreateForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  label='Город')
    programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all(),
                                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                                  label='Специальность')
    url = forms.CharField(label='URL',
                          widget=forms.URLInput(attrs={'class': 'form-control'})
                          )
    company = forms.CharField(label='Компания',
                              widget=forms.TextInput(attrs={'class': 'form-control'})
                              )
    description = forms.CharField(label='Описание',
                                  widget=forms.Textarea(attrs={'class': 'form-control'})
                                  )

    class Meta:
        model = Vacancy
        fields = '__all__'

