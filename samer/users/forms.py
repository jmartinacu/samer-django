from django import forms


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'user',
            'placeholder': ' ',
        }
    ))
    pwd = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'id': 'pwd',
            'placeholder': ' ',
        }
    ))


class SigninForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'user',
            'placeholder': ' ',
        }
    ))
    pwd = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'id': 'pwd',
            'placeholder': ' ',
        }
    ))


class AdminSiginForm(forms.Form):
    user = forms.CharField(label='Nombre de usuario')
    pwd = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    email = forms.EmailField(label='Correo electronico')
    name = forms.CharField(label='Nombre')
    surname = forms.CharField(label='Apellido')
