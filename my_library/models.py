from operator import mod
from django.db import models


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



