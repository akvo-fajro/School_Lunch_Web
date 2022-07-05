from django import forms

# this is the class for user to login
class LoginForm(forms.Form):
    username = forms.CharField(
        label='帳號',
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput()
    )

# this is the classs for user to change there password
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="新的密碼",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='確認密碼',
        widget=forms.PasswordInput()
    )