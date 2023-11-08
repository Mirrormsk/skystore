from django import forms
from django.forms import inlineformset_factory

from catalog.models import Version, Product


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
