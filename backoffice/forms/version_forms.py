from django import forms
from django.forms import inlineformset_factory

from catalog.models import Version, Product


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        exclude = ('is_active',)


VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1, can_delete_extra=False)
