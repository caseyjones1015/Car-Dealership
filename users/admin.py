from django.contrib import admin
from .models import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Display user and role in the admin list
    # Add more configurations as needed

# Register your models here.
