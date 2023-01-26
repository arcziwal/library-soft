from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


class SearchBook(forms.Form):
    title = forms.CharField(label="Wyszukiwana fraza", max_length=128)
    factors = forms.ChoiceField(label="Wyszukaj po:", choices=FACTORS)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Login do posługiwania się na stronie. Max. 30 znaków',
            'password': 'min. 8 znaków',
            'password2': 'Potwierdź hasło',
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

