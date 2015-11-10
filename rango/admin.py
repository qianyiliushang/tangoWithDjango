from django.contrib import admin
from .models import Category, Page,UserProfile

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):

    """add model category to admin page"""
    # fieldsets = [
    #     ("Brief Inro": {'fields': ['name']}),
    #     ("Favorites": {'fields': ['views', 'likes']})
    # ]

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'views', 'likes','slug')

class PageAdmin(admin.ModelAdmin):

    """add model page to admin page"""
    # fieldsets = [
    #     (None, {'fields': ['category']}),
    #     ('Page info': {'fields': ['title', 'url', 'views']})
    # ]
    list_display = ('category', 'title', 'url', 'views')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
