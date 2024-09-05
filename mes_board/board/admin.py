from django.contrib import admin
from .models import Message, Author

admin.site.register(Message)
admin.site.register(Author)