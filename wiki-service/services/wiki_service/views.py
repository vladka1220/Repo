from rest_framework import viewsets, permissions
from .models import WikiPage
from .serializers import WikiPageSerializer


class WikiPageViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы со страницами вики.
    """

    queryset = WikiPage.objects.all()
    serializer_class = WikiPageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает только те страницы, которые создал текущий пользователь.
        """
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя в качестве автора при создании страницы.
        """
        serializer.save(author=self.request.user)
