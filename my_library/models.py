from operator import mod
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True)
    death_date = models.DateField(null=True)


class PublishingHouse(models.Model):
    name = models.CharField(max_length=64)


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ManyToManyField(Author, default='nieznany')
    num_of_pages = models.SmallIntegerField(null=True)
    publishing_date = models.DateField(null=True)
    isbn = models.CharField(max_length=13, null=True)
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True)


