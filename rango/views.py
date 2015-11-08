from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page

# Create your views here.


def index(request):
    # return HttpResponse("Rango says hey there world <br><a href =
    # '/rango/about'>About </a>")
    category_list = Category.objects.order_by('-likes')
    context_dict = {"categories": category_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # return HttpResponse(content=b'Somthing about tango<br><a
    # href="/rango">Rango Home</a>')
    context = {"about": "I'm rango, have you ever heard me?"}
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)
