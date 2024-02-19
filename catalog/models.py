from django.urls import reverse
from django.db import models


# Model for different art categories
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Museum(models.Model):
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='museum_images/')
    title = models.CharField(max_length=255, null=True)
    email = models.EmailField(default='example@example.com')
    password = models.CharField(max_length=128, blank=True, null=True)
    contact_email = models.EmailField(default='example@example.com')
    contact_phone = models.CharField(max_length=20, null=True)
    opening_hours = models.TextField(null=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


# Model for individual artworks
class Artifact(models.Model):
    title = models.CharField(max_length=200, null=True)
    artist = models.CharField(max_length=200, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='artwork_images/')
    categories = models.ManyToManyField(Category)  # Many-to-Many relationship with Category
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)  # Foreign Key to Museum model
    date_created = models.DateField(null=True)
    century = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class Meta:
    app_label = 'catalog'
