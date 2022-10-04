from django import forms
from django.forms.widgets import Input

from .models import Order, CallBack, ReviewsUs
import re

class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('name', 'phone_number',)
        labels = {
            'name': '',
            'phone_number': '',
        }
        help_texts = {
            'name': 'Имя',
            'phone_number': 'Номер телефона'
        }
        widgets = {
            'name': Input(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'phone_number': Input(attrs={'placeholder': '+375291234567'})
        }
    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']
        if not re.findall(r'(^\s*\+?375((33\d{7})|(29\d{7})|(44\d{7}|)|(25\d{7}))\s*$)', number):
            raise forms.ValidationError('Введите, пожалуйста, номер в формате +375291234567')
        return number

class CallBackForm(forms.ModelForm):

    class Meta:
        model = CallBack
        fields = ('name', 'phone_number')
        labels = {
            'name': '',
            'phone_number': '',
        }
        help_texts = {
            'name': 'Имя',
            'phone_number': 'Номер телефона'
        }
        widgets = {
            'name': Input(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'phone_number': Input(attrs={'placeholder': '+375291234567'})
        }

class ReviewsUsForm(forms.ModelForm):

    class Meta:
        model = ReviewsUs
        fields = ('name', 'phone_number', 'pet', 'reviews_us')
        labels = {
            'name': '',
            'phone_number': '',
            'pet': '',
            'reviews_us': '',
        }
        help_texts = {
            'name': 'Имя',
            'phone_number': 'Номер телефона',
            'pet': 'Имя питомца',
            'reviews_us': 'Ваш отзыв',
        }
        widgets = {
            'name': Input(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'phone_number': Input(attrs={'placeholder': '+375291234567'}),
            'pet': Input(attrs={'placeholder': 'Собака Цезарь'}),
            'reviews_us': Input(attrs={'placeholder': 'Ваш отзыв'}),
        }
