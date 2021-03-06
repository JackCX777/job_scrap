from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from scrap.models import City, ProgrammingLanguage

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()
        if email and password:
            query_set = User.objects.filter(email=email)
            if not query_set.exists():
                raise forms.ValidationError('Вы не зарегестрированы!')
            if not check_password(password, query_set[0].password):
                raise forms.ValidationError('Не верный пароль!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Даннный пользователь отключен!')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Введите адрес почты', widget=forms.EmailInput(attrs={'class': 'form-control'})
                            )
    password = forms.CharField(
        label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    password2 = forms.CharField(
        label='Введите пароль еще раз', widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадяют!')
        return data['password2']


class UserPreferenceForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name="slug",
                                  required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  label='Город')
    programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all(),
                                                  to_field_name="slug",
                                                  required=True,
                                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                                  label='Специальность')
    send_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='Получать рассылку?'
                                   )

    class Meta:
        model = User
        fields = ('city', 'programming_language', 'send_email',)


class ContactForm(forms.Form):
    city = forms.CharField(
                                  required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  label='Город'
    )
    programming_language = forms.CharField(
                                                  required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                                  label='Специальность'
    )
    email = forms.EmailField(label='Введите адрес почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))
