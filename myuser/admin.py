from django.contrib import admin
from myuser.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']

    class Meta:
        model = CustomUser
        fields = '__all__'
