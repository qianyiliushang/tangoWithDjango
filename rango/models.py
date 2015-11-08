from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class Category(models.Model):

    """Category models"""
    name = models.CharField(max_length=120, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):

    """page models"""

    category = models.ForeignKey(Category)
    title = models.CharField(max_length=120)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self,):
        return self.title
