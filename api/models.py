from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, blank=True, null=True, related_name='category_titles')
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genres, blank=True)
    
    
    def __str__(self):
        return self.name
