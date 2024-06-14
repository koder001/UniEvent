from django import forms
from .models import UserProfile, Group

class LoginForm(forms.Form):
    """Форма для входа пользователя."""
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class ProfileRegistrationForm(forms.ModelForm):
    """Форма для создания пользователя."""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    email = forms.EmailField(max_length=254)
    group_student = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), required=False, widget=forms.Select(attrs={'style': 'max-width: 20ch;'}))

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'group_student', 'year_of_admission', 'password', 'password2']

    def clean_email(self):
        """Проверяет, не используется ли уже email."""
        data = self.cleaned_data['email']
        if UserProfile.objects.filter(email=data).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return data

    def clean_password2(self):
        """Проверяет, совпадают ли пароли."""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class ProfileEditForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""
    group_student = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), required=False, widget=forms.Select(attrs={'style': 'max-width: 20ch;'}))
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'patronymic', 'group_student', 'year_of_admission', 'email']
