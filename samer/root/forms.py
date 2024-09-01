from django import forms

from samer.posts.models import ParsedPost


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadPost(forms.Form):
    file = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        )
    )
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )
    des = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input description-form",
                "id": "des",
                "placeholder": " ",
            }
        ),
    )


class EditPost(forms.Form):
    file = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        ),
    )
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )
    des = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input description-form",
                "id": "des",
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        post: ParsedPost = kwargs.pop("post", None)
        super().__init__(*args, **kwargs)
        if post is not None:
            self.fields["des"].initial = post["description"]
            self.fields["name"].initial = post["name"]


class AdminForm(forms.Form):
    user = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "id": "user",
                "placeholder": " ",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "id": "email",
                "placeholder": " ",
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "id": "name",
                "placeholder": " ",
            }
        )
    )
    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "id": "surname",
                "placeholder": " ",
            }
        )
    )
    pwd = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "id": "pwd",
                "placeholder": " ",
            }
        )
    )


class CreateTag(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        )
    )
    name = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )

    ids = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "ids",
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        ids: str = kwargs.pop("ids", "")
        init = kwargs.pop("init", False)
        super().__init__(*args, **kwargs)
        if init:
            self.fields["ids"].initial = ids
