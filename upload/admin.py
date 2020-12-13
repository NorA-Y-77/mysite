from django.contrib import admin
from .models import Image

# Register your models here.
@admin.register(Image)
class UploadImgAdmin(admin.ModelAdmin):
    list_display = ('pk' ,'photo')