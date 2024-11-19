from rest_framework import serializers
from .models import WikiPage


class WikiPageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели WikiPage.
    """

    class Meta:
        model = WikiPage
        fields = ["id", "title", "content", "author", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
