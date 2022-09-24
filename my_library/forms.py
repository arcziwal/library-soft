from django import forms
from .models import Author, PublishingHouse
import library_soft.settings

FACTORS = (
    (1, 'tytule'),
    (2, 'autorze'),
    (3, 'wydawnictwie'),
    (4, 'ISBN'),
)


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


class NewBookForm(forms.Form):
    title = forms.CharField(label="Tytuł:", max_length=128)
    author = forms.ModelChoiceField(queryset=Author.objects.all(), label="Autor")
    num_of_pages = forms.IntegerField(max_value=9999, label="Liczba stron", help_text="Zakres: 0-9999", required=False)
    publishing_date = forms.IntegerField(
        min_value=0,
        max_value=2022,
        label="Rok wydania",
        help_text="Zakres: 0-2022",
        required=False
    )
    isbn = forms.CharField(max_length=13, label="Numer ISBN", help_text="8 lub 13 cyfrowy")
    publishing_house = forms.ModelChoiceField(queryset=PublishingHouse.objects.all())


class SearchByTitle(forms.Form):
    title = forms.CharField(label="Wyszukiwana fraza", max_length=128)
    factors = forms.ChoiceField(label="Wyszukaj po:", choices=FACTORS)


