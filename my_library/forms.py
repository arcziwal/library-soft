from django import forms

import library_soft.settings


class NewAuthorForm(forms.Form):
    first_name = forms.CharField(label="Imię (Imiona):", max_length=64)
    last_name = forms.CharField(label="Nazwisko", max_length=64)
    birth_date = forms.DateField(
        label="Data urodzenia (DD.MM.RRRR)",
        required=False,
        input_formats=library_soft.settings.DATE_INPUT_FORMATS,
    )
    death_date = forms.DateField(
        label="Data śmierci (DD.MM.RRRR)",
        required=False,
        input_formats=library_soft.settings.DATE_INPUT_FORMATS,
    )


class NewPublishingHouseForm(forms.Form):
    name = forms.CharField(label="Nazwa wydawnictwa", max_length=64)
