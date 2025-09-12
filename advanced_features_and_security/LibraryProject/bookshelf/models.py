from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

#class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, date_of_birth=None, password=None, **extra_fields): pass
#     def create_superuser(self, username, email, date_of_birth=None, password=None, **extra_fields): pass
# class CustomUser(AbstractUser):
#     date_of_birth = models.DateField(null=True, blank=True)
#     profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
