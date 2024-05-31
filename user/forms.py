from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
	"""Форма для входа пользователя."""
	email = forms.EmailField(label="Email")
	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class ProfileRegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действительный адрес электронной почты.')

	class Meta:
		model = UserProfile
		fields = ['first_name', 'last_name', 'patronymic', 'group_student', 'email', 'photo', 'password', 'password2']

	def clean_password2(self):
		"""Проверяет, совпадают ли пароли."""
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Пароли не совпадают.')
		return cd['password2']

	def clean_email(self):
		"""Проверяет, не используется ли уже email."""
		data = self.cleaned_data['email']
		if UserProfile.objects.filter(email=data).exists():
			raise forms.ValidationError('Этот адрес электронной почты уже используется.')
		return data


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['first_name', 'last_name', 'patronymic', 'group_student', 'email', 'photo']
