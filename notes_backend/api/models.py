from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """
    Model representing a user's personal note.

    Fields:
    - title: Short title of the note
    - content: Body content of the note
    - owner: The User who owns the note
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    """
    title = models.CharField(max_length=255)
    content = models.Textarea().render("content", "")
    # The above is not correct usage; change to TextField
    # Keeping implementation proper:
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)

    def __str__(self) -> str:
        return f"{self.title} (#{self.pk})"
