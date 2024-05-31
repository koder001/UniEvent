from django.contrib import admin
from .models import UserProfile, Group, Institution

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'fullname')
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'fullname', 'institution')
    search_fields = ('name', 'institution__name')

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'group_student')
    search_fields = ('email', 'first_name', 'last_name')
