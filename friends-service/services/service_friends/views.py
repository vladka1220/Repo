from rest_framework.decorators import action
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Friend, FriendRequest, FavoriteUser
from .serializers import FriendProfileSerializer
from config.messages_config.error_messages import get_message
from .services import ProfileMicroserviceClient
from django.conf import settings
from .pagination import CustomPagination


class FriendsListView(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка друзей.
    Если передан user_id, то получаем список друзей для этого юзера, если
    user_id не передан, то получаем список друзей для юзера, сделавшего запрос.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = self.request.GET.get(
            'user_id', self.request.user.id
        )
        friends_ids = Friend.objects.filter(
            user=user_id
        ).order_by("-created_at").values_list('friend', flat=True)
        params = {"ids": ",".join(map(str, friends_ids))}
        client = ProfileMicroserviceClient()
        friends = client.get_data_from_microservice(
            endpoint=settings.PROFILE_USERS_BY_LIST_IDS,
            params=params,
        )
        if not friends:
            return Response(
                {"detail": get_message("not_found")},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FriendProfileSerializer(
            data=friends['results'],
            many=True
        )
        if not serializer.is_valid():
            return Response(
                {
                    "detail": "Invalid data received from the profile service",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(paginated_data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Поиск друзей юезар из запроса по частичному совпадению с именем,
        юзернеймом, фамилией. Запрос "ха" -> "Михаил" "Харитонов" "Хакер".
        """
        query = request.query_params.get("q", "")
        if query:
            friends_ids = Friend.objects.filter(
                user=self.request.user.id
            ).values_list('friend', flat=True)
            params = {"ids": ",".join(map(str, friends_ids)), 'name': query}
            client = ProfileMicroserviceClient()
            friends = client.get_data_from_microservice(
                endpoint=settings.PROFILE_USERS_SEARCH,
                params=params,
            )
        if not friends['results']:
            return Response(
                {"detail": get_message("friend_not_found")},
                status=200
            )
        serializer = FriendProfileSerializer(
            data=friends['results'],
            many=True
        )
        if not serializer.is_valid():
            return Response(
                {
                    "detail": "Invalid data received from the profile service",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)


class FriendDeleteView(views.APIView):
    """
    Удаление друга.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id=None):
        try:
            friend = Friend.objects.get(user=request.user.id, friend=user_id)
            friend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Friend.DoesNotExist:
            return Response(
                {"detail": get_message("friend_not_found")},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class FriendRequestViewSet(viewsets.ViewSet):
    """
    Создание запроса на добавление в друзья
    """
    permission_classes = [IsAuthenticated]

    def create(self, request, user_id=None):
        client = ProfileMicroserviceClient()
        check_user = client.get_data_from_microservice(
            endpoint=f'{settings.PROFILE_USER_CHECK}{user_id}/',
        )
        if not check_user.get('exists'):
            return Response(
                {"detail": get_message("invalid_user_id")},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.pk == user_id:
            return Response(
                {"detail": get_message("cannot_send_request_to_self")},
                status=status.HTTP_409_CONFLICT
            )

        if Friend.objects.filter(
            user=request.user.id, friend=user_id
        ).exists():
            return Response(
                {"detail": get_message("already_friends")},
                status=status.HTTP_400_BAD_REQUEST
            )

        if FriendRequest.objects.filter(
            from_user=request.user.id,
            to_user=user_id
        ).exists():
            return Response(
                {"detail": get_message("friend_request_already_sent")},
                status=status.HTTP_400_BAD_REQUEST
            )

        FriendRequest.objects.create(
            from_user=request.user.id,
            to_user=user_id
        )
        return Response(
            {"detail": get_message("friend_request_sent")},
            status=status.HTTP_201_CREATED
        )

    def approve(self, request, user_id=None):
        """
        Одобрение запроса на добавление в друзья.
        """
        try:
            friend_request = FriendRequest.objects.get(
                from_user=request.user.id, to_user=user_id, is_accepted=False
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"detail":  get_message("friend_request_not_found")},
                status=status.HTTP_404_NOT_FOUND
            )
        friend_request.is_accepted = True
        friend_request.save()

        Friend.objects.create(
            user=request.user.id,
            friend=user_id
        )
        Friend.objects.create(
            user=user_id,
            friend=request.user.id
        )

        return Response(
            {"detail": "Friend request approved"},
            status=status.HTTP_200_OK
        )


class FavoriteUserView(views.APIView):
    """
    Управление избранными пользователями.
    """

    permission_classes = [IsAuthenticated]  # Проверка аутентификации

    def post(self, request, user_id):
        """
        Обработка POST-запроса для добавления пользователя в избранное.
        """
        client = ProfileMicroserviceClient()
        check_user = client.get_data_from_microservice(
            endpoint=f'{settings.PROFILE_USER_CHECK}{user_id}/',
        )
        if not check_user.get('exists'):
            return Response(
                {"detail": get_message("invalid_user_id")}, status=400
            )

        if FavoriteUser.objects.filter(
            user=request.user.id, favorite=user_id
        ).exists():
            return Response(
                {"detail": get_message("favorite_already_added")}, status=400
            )

        FavoriteUser.objects.create(
            user=request.user.id,
            favorite=user_id
        )
        return Response(
            {"detail": get_message("favorite_added")}, status=201
        )

    def delete(self, request, user_id):
        """
        Обработка DELETE-запроса для удаления из избранного.
        """
        try:
            favorite = FavoriteUser.objects.get(
                user=request.user,
                favorite=user_id
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FavoriteUser.DoesNotExist:
            return Response(
                {"detail": get_message("favorite_not_found")}, status=404
            )
        except Exception:
            return Response(
                {"detail": get_message("forbidden_action")}, status=403
            )
