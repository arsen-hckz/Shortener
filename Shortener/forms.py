from django import forms

class ShortenerForm(forms.Form):
    long_url = forms.URLField(max_length=2000,widget=forms.URLInput(attrs={"class": "input", "placeholder": "https://example.com"}))
    custom_code = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "custom-alias"
        })
    )

