from django.contrib import admin
from apps.users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_id', 'email', 'username')  # Fields shown in admin list view
    search_fields = ('email', 'username')               # Optional: makes search box useful
    ordering = ('id',) 