# notes/admin.py
from django.contrib import admin
from .models import Note

# Register the Note model with the admin site.
# Note model
admin.site.register(Note)
