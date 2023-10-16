from django import forms
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'full_name', 'email', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea()}

        labels = {
            'full_name': 'نام و نام خانوادگی شما',
            'email': 'ایمیل شما'
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی اجباری است. لطفا وارد نمایید'
            }
        }
