from django import forms


class UploadImagePost(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(
        attrs={
            'class': 'image-form',
            'style': 'display: none',
        }
    ))
    des = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'input description-form',
                'id': 'des',
                'placeholder': ' ',
            }
        )
    )
