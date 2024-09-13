from django.contrib import admin
from myuser.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
  class Meta:
    model = CustomUser
    fields = '__all__'