from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'value': 1,
    }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CartRemoveProduct(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'value': 1,
    }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

