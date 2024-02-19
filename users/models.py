from django.contrib.auth.models import User, Group, Permission
from django.db import models
from PIL import Image  # Add this import statement
from catalog.models import Category, Museum


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='media/profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    email = models.EmailField(default='example@example.com')
    password = models.CharField(max_length=128, blank=True, null=True)
    categories_of_interest = models.ManyToManyField(Category)  # Many-to-Many relationship with Category
    last_sign_in = models.DateTimeField(auto_now=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='profile_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='profile_user_permissions', blank=True)

    def __str__(self):
        return self.user.username
