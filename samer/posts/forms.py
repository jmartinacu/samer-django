from django import forms


class CreateCommentForm(forms.Form):
    comment: str = forms.CharField(
        label='Crea un comentario',
        widget=forms.Textarea(attrs={
            'onkeydown': 'submitFormOnEnter(event)',
            'placeholder': 'Añade un nuevo comentario',
            'oninput': 'autoResize(this)',
            'class': 'create-comment-textarea'
        })
    )
