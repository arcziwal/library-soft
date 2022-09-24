from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import forms, models


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass


class NewAuthor(View):
    def get(self, request):
        form = forms.NewAuthorForm()
        return render(request, 'new_author_form.html', {'form': form})

    def post(self, request):
        form = forms.NewAuthorForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birth_date = form.cleaned_data['birth_date']
            death_date = form.cleaned_data['death_date']
            author = models.Author.objects.create(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                death_date=death_date
            )
            return HttpResponse(f"""
                <p>Autor {author.first_name} {author.last_name} został dodany do bazy danych</p>
                <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p> 
            """)
        else:
            return HttpResponse("Błąd! Nie dodano do bazy danych")


