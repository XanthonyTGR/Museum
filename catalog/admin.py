from django.contrib import admin

from .models import Category, Museum, Artifact
from users.models import UserProfile

admin.site.register(Category)
admin.site.register(Museum)
admin.site.register(Artifact)
admin.site.register(UserProfile)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MuseumAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description', 'contact_email', 'contact_phone', 'opening_hours', 'website')
    search_fields = ('name', 'location', 'description', 'contact_email', 'contact_phone', 'opening_hours', 'website')


class ArtifactAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'get_museum', 'get_category')
    search_fields = ('title', 'artist', 'museum__name', 'category__name')
    list_filter = ('museum', 'category')

    def get_museum(self, obj):
        return obj.museum.name

    def get_category(self, obj):
        return obj.category.name


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_bio')
    search_fields = ('user__username', 'bio')

    def get_bio(self, obj):
        return obj.bio