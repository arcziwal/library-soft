from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass


class New_author(View):
    def get(self, request):
        return render(request, 'new_author_form.html')

    def post(self, request):
        pass
