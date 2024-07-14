from django.contrib import admin # type: ignore
from .models import User

# Register your models here.

admin.site.register(User)
