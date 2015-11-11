from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.


def index(request):
    # return HttpResponse("Rango says hey there world <br><a href =
    # '/rango/about'>About </a>")
    # request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')
    most_viewed_pages = Page.objects.order_by('-views')[:5]
    html_template = 'rango/index.html'
    #visit = int(request.COOKIES.get('visit', '1'))
    #reset_last_visit_time = False
    context_dict = {"categories": category_list,
                    "most_viewed_pages": most_viewed_pages
                    }
    # use client side cookies
    # if 'last_visit' in request.COOKIES:
    #     last_visit = request.COOKIES['last_visit']
    #     last_visit_time = datetime.strptime(
    #         last_visit[:-7], '%Y-%m-%d %H:%M:%S')
    #     if (datetime.now() - last_visit_time).seconds > 5:
    #         visit = visit + 1
    #         reset_last_visit_time = True
    # else:
    #     reset_last_visit_time = True
    #     context_dict['last_vist'] = visit
    #     response = render(request, html_template, context_dict)
    # if reset_last_visit_time:
    #     response.set_cookie('last_visit', datetime.now())
    #     response.set_cookie('visit', visit)

    # Use server side cookies
    visit = request.session.get('visit')

    if not visit:
        visit = 1
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_visit).seconds > 10:
            visit = visit + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visit'] = visit
    context_dict['visit'] = visit
    response = render(request, html_template, context_dict)
    return response


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


@login_required
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


@login_required
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
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm
    context = {'form': form,
               'category': cat}
    return render(request, 'rango/add_page.html', context)


def register(request):
    # if request.session.test_cookie_worked():
    #     print "Test cookie worked"
    #     request.session.delete_test_cookie()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form,
               'profile_form': profile_form,
               'registered': registered}
    return render(request, 'rango/register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your rango account is disabled')
        else:
            print 'Invalid login, details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
