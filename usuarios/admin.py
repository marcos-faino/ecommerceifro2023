from django.contrib import admin
from .models import MeuUser


@admin.register(MeuUser)
class MeuUserAdmin(admin.ModelAdmin):
    pass

