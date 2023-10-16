from django import forms
from django.core.exceptions import ValidationError

from account_module.models import User


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(),

            'about_user': forms.Textarea()

        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام حانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
            'about_user': 'درباره شخص'
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    confirm_new_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password == confirm_new_password:
            return confirm_new_password
        else:
            raise ValidationError('کلمه عبور و تکرار آن مغایرت دارد')
