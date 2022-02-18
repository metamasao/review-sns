from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow,Action 
from .forms import CustomUserCreationForm, CustomUserChangeFormForAdmin

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeFormForAdmin
    model = CustomUser
    list_display = ('username', 'email', 'is_active',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
admin.site.register(Action)



