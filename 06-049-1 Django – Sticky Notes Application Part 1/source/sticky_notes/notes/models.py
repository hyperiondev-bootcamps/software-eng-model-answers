# notes/models.py
from django.db import models


class Note(models.Model):
    """
    Model representing a sticky note.

    Fields:
    - title: CharField for the note title with a maximum length of 255 characters.
    - content: TextField for the sticky note content.
    - created_at: DateTimeField set to the current date and time when the note is created.

    Methods:
    - __str__: Returns a string representation of the note, showing the title.

    :param models.Model: Django's base model class.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
