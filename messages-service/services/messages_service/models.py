from mongoengine import Document, fields
from mongoengine.queryset import QuerySet


class Message(Document):
    """
    Модель сообщения, хранящаяся в MongoDB.

    Атрибуты:
        sender (str): Идентификатор отправителя сообщения.
        recipient (str): Идентификатор получателя сообщения.
        content (str): Содержимое сообщения.
        timestamp (datetime): Временная метка отправки сообщения.
    """

    sender = fields.StringField(required=True)
    recipient = fields.StringField(required=True)
    content = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True)

    meta = {
        "collection": "messages",  # Название коллекции в MongoDB
        "indexes": [
            {"fields": ["sender"]},
            {"fields": ["recipient"]},
            {"fields": ["timestamp"]},
        ],
    }

    @classmethod
    def _qs(cls):
        """Возвращает объект запроса для текущего класса документа."""
        if not hasattr(cls, "__objects"):
            queryset_class = cls.meta.get("queryset_class", QuerySet)
            cls.__objects = queryset_class(cls, cls._get_collection())
        return cls.__objects

    @property
    def objects(self):
        """Возвращает объект запроса для текущего класса документа."""
        return self._qs()
