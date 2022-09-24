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
            return HttpResponse("""
                Błąd! Nie dodano do bazy danych
                <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p> 
                """)


class NewPublishingHouse(View):
    def get(self, request):
        form = forms.NewPublishingHouseForm()
        return render(request, 'new_publishing_house_form.html', {'form': form})

    def post(self, request):
        form = forms.NewPublishingHouseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pub_house = models.PublishingHouse.objects.create(name=name)
            return HttpResponse(f"""
            <p>Wydawnictwo {pub_house.name} zostało dodane do bazy danych</p>
            <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p>
            """)
        else:
            return HttpResponse("""
            Błąd! Nie dodano do bazy danych
            <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p> 
            """)


class NewBook(View):
    def get(self, request):
        form = forms.NewBookForm()
        return render(request, 'new_book_form.html', {'form': form})

    def post(self, request):
        form = forms.NewBookForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("Form valid")
            print(type(form.cleaned_data['author']))
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            num_of_pages = form.cleaned_data['num_of_pages']
            publishing_year = form.cleaned_data['publishing_date']
            isbn = form.cleaned_data['isbn']
            publishing_house = form.cleaned_data['publishing_house']
            book = models.Book.objects.create(
                title=title,
                num_of_pages=num_of_pages,
                publishing_year=publishing_year,
                isbn=isbn,
                publishing_house=publishing_house,
            )
            book.author.add(author)
            book.save()
            return HttpResponse(f"""
                Książka {book.title} autorstwa {author} została dodana do bazy danych pod numerem: {book.pk}
                <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p>
            """)
        else:
            print(form.errors.as_data())
            return HttpResponse("""
                Błąd! Nie dodano do bazy danych
                <p>Naciśnij <a href="/">tutaj</a> aby powrócić na stronę główną</p> 
                """)


class SearchByTitle(View):
    def get(self, request):
        form = forms.SearchByTitle()
        return render(request, 'browser.html', {'form': form})


class SearchResults(View):
    def get(self, request):
        form = forms.SearchByTitle(request.GET)
        if form.is_valid():
            title = form.cleaned_data['title']
            factor = form.cleaned_data['factors']
            if factor == "1":
                list_of_books = models.Book.objects.filter(title__icontains=title)
                return render(request, 'search_results.html', {'book_list': list_of_books})




