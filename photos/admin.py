from django.contrib import admin

# Register your models here.

from .models import Photo, Category, Food

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Food)
