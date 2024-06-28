from django.contrib import admin
from .models import Academia

class AcademiaAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'major', 'interests')

# Register your models here.

admin.site.register(Academia, AcademiaAdmin)