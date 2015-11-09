from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Page
from .forms import CategoryForm, PageForm


# Create your views here.


def index(request):
    # return HttpResponse("Rango says hey there world <br><a href =
    # '/rango/about'>About </a>")
    category_list = Category.objects.order_by('-likes')
    most_viewed_pages = Page.objects.order_by('-views')
    context_dict = {"categories": category_list,
                    "most_viewed_pages": most_viewed_pages
                    }
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # return HttpResponse(content=b'Somthing about tango<br><a
    # href="/rango">Rango Home</a>')
    context = {"about": "I'm rango, have you ever heard me?"}
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):
    context_dict = {}
    category = Category.objects.get(slug=category_name_slug)
    context_dict['category_name'] = category.name

    pages = Page.objects.filter(category=category)
    context_dict['pages'] = pages
    context_dict['category'] = category
    category_not_found = get_object_or_404(Category, slug=category_name_slug)
    context_dict['category_not_found'] = category_not_found
   # context_dict['category_name_slug'] = category_name_slug
    # except Category.DoesNotExist:
    # pass
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category=cat
                page.views = 0
                page.save()
                return category(request,category_name_slug)
        else:print form.errors
    else:form = PageForm
    context = {'form':form,
               'category':cat}
    return render(request,'rango/add_page.html',context)
