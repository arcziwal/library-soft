from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
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


class SearchBook(View):
    def get(self, request):
        form = forms.SearchBook()
        return render(request, 'browser.html', {'form': form})


class SearchResults(View):
    def get(self, request):
        form = forms.SearchBook(request.GET)
        if form.is_valid():
            phrase = form.cleaned_data['title']
            factor = form.cleaned_data['factors']
            if factor == "1":
                list_of_books = models.Book.objects.filter(title__icontains=phrase)
            elif factor == "2":
                list_of_books = models.Book.objects.filter(author__last_name__icontains=phrase)
            elif factor == "3":
                list_of_books = models.Book.objects.filter(publishing_house__name__icontains=phrase)
            elif factor == "4":
                list_of_books = models.Book.objects.filter(isbn=phrase)
            else:
                list_of_books = []
            if not list_of_books:
                records_info = "Brak znalezionych rekordów spełniających wyszukiwaną frazę"
            else:
                records_info = "Znaleziono następujące rekordy w bazie danych:  "
            return render(request, 'search_results.html', {'book_list': list_of_books, "records_info": records_info})


class BookDetails(View):
    def get(self, request, **kwargs):
        number = kwargs['number']
        book = models.Book.objects.get(pk=number)
        author = models.Author.objects.get(book=book)
        return render(request, 'book_details.html', {'book': book, 'author': author})


class CreateUser(View):
    def get(self, request):
        form = forms.NewUserForm()
        return render(request, 'register_form.html', {'register_form': form})

    def post(self, request):
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Pomyślnie zarejstrowano")
            return redirect("index-page")
        messages.error(request, "Operacja nieudana. Nieprawidłowe dane")


class LoginRequest(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, template_name='login.html', context={'login_form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Użytkownik {username} został poprawnie zalogowany")
                return redirect('index-page')
            else:
                messages.error(request, "Błędny login lub hasło")
                return redirect('/login')
        else:
            messages.error(request, "Błędny login lub hasło")
            return redirect('/login')


class LogoutRequest(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Zostałeś prawidłowo wylogowany")
        return redirect("/login")


class UserDetails(View):
    def get(self, request):
        return render(request, template_name="user_details.html", context={})
