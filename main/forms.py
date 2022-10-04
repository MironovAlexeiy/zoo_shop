from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# class FormRegistration(forms.Form):
#     username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'id': "inputUsername"
#     }))
#     password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'id': 'inputPassword',
#     }))
#     rep_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'id': 'ReInputPassword'
#     }))
#     email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
#         'class': 'form-control',
#         'id': 'ReInputPassword'}))
#
#
#
#     def clean(self):
#         password = self.cleaned_data['password']
#         confirm_password = self.cleaned_data['rep_password']
#         if password != confirm_password:
#             raise forms.ValidationError('Пароли не совпали! Попробуйте ещё раз.')
#
#     def save(self):
#         client = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             password=self.cleaned_data['rep_password'],
#             email=self.cleaned_data['email']
#         )
#         client.save()
#         auth = authenticate(**self.cleaned_data)
#         return auth
#
# class Sign(forms.Form):
#     email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
#         'class': 'form-control mt-2',
#         'id': 'inputEmail',
#         'placeholder': 'Email'}))
#     password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
#         'class': 'form-control mt-2',
#         'id': 'inputPassword',
#         'placeholder': 'Пароль'
#     }))

