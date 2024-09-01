from django import forms


class CreateCommentForm(forms.Form):
    comment: str = forms.CharField(
        label="Crea un comentario",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Comenta algo nuevo...",
                "class": "create-comment-textarea",
                "id": "create-comment-form",
            }
        ),
    )
