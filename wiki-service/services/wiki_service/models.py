from django.db import models
from django.contrib.auth.models import User


class WikiPage(models.Model):
    """
    Модель для хранения страниц вики.
    """

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated_at"]
