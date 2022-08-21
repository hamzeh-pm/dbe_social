import io

import requests
from django import forms
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "title",
            "url",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("the given url does not valid")

        return url

    def save(self, commit=True, *args, **kwargs):
        image = super().save(commit=False)
        image_name = (
            slugify(self.cleaned_data["title"])
            + "."
            + self.cleaned_data["url"].rsplit(".", 1)[1].lower()
        )
        resp = requests.get(self.cleaned_data["url"])
        image.image.save(image_name, io.BytesIO(resp.content), save=False)
        if commit:
            image.save()
        return image
