from django import forms


class UploadImagePost(forms.Form):
    image_post = forms.ImageField(label='Imagen publicación')
