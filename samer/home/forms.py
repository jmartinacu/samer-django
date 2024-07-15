import math

from django import forms

from samer.home.models import profile as mongo_profile

WITDH_LINES = 350

CHARACTERS_PER_LINE = 32


class ProfileForm(forms.Form):
    app_name: str = forms.CharField(widget=forms.TextInput(),)
    app_real_name: str = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'app-real-name-form'
            }
        ),
    )
    descriptions: str = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'descriptions-form',
                'style': '',
            }
        ),
    )
    url: str | None = forms.CharField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'url-form',
            }
        ),
    )
    image_url = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'image-url-form',
        })
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        profile = list(mongo_profile.find(query={}))[0]
        description_text = '\n'.join(profile['descriptions'])
        num_lines = sum([
            math.ceil(len(description)/CHARACTERS_PER_LINE)
            for description in profile['descriptions']
        ])
        self.fields['descriptions'].widget.attrs.update({
            'style': (
                f'width: {WITDH_LINES}px;'
                f'height: {num_lines*18}px;'
            )
        })
        initial_values = {
            'app_name': profile['app_name'],
            'app_real_name': profile['app_real_name'],
            'descriptions': description_text,
            'url': profile['url'],
        }
        for field, initial_value in initial_values.items():
            if field in self.fields:
                self.fields[field].initial = initial_value
