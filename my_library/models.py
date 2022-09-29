import uuid
from operator import mod
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True)
    death_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PublishingHouse(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ManyToManyField(Author, default='nieznany')
    num_of_pages = models.SmallIntegerField(null=True)
    publishing_year = models.IntegerField(null=True)
    isbn = models.CharField(max_length=13, null=True)
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True)
    is_borrowed = models.BooleanField(default=False)
    adding_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        try:
            author = self.author.all()
            print(author)
            return f"{self.title} - {author[0]}"
        except IndexError:
            return f"{self.title}"


class LibraryUser(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    user_id = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    borrowed_books = models.ManyToManyField(Book, through='BorrowedBooks', null=True, related_name='borrowed_books')
    reserved_books = models.ManyToManyField(Book, through='ReservedBooks', null=True, related_name='reserved_books')
    creation_date = models.DateField(auto_now_add=True)


class BorrowedBooks(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    bor_user = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, related_name='bor_users', null=True)
    bor_book = models.ForeignKey(Book, on_delete=models.SET_NULL, related_name='bor_books', null=True)


class ReservedBooks(models.Model):
    reserve_date = models.DateField(auto_now_add=True)
    res_user = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, related_name='res_users', null=True)
    res_book = models.ForeignKey(Book, on_delete=models.SET_NULL, related_name='res_books', null=True)






