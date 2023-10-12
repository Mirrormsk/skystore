from django.shortcuts import render

from .services import messages_saver


# Create your views here.


def index(request):
    """Функция отображения главной страницы"""
    return render(request, "catalog/index.html", {'nbar': 'home'})


def contacts(request):
    """Функция отображения страницы контактов"""
    if request.method == "POST":
        print(request.POST)
        messages_saver.save_message(request.POST)

    return render(request, "catalog/contacts.html", {'nbar': 'contacts'})
