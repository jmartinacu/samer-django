from django import forms


class UploadImagePost(forms.Form):
    name = forms.CharField(label='Nombre publicación')
    image_post = forms.ImageField(label='Imagen publicación')
