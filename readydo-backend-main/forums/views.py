from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.dates import server_now
from common.manual_parameters import FORUM_ID
from forums.models import Forum, Message
from forums.serializers import ForumSerializer, MessageSerializer


class ForumAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class ForumMessageAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        forum_id = self.request.query_params.get('forum_id')
        return Message.objects.filter(forum=int(forum_id))

    @swagger_auto_schema(manual_parameters=[FORUM_ID])
    def get(self, request, *args, **kwargs):
        forum = Forum.objects.filter(id=int(self.request.query_params.get('forum_id')))
        if forum:
            return self.list(request, *args, **kwargs)
        else:
            return Response({'message': 'User doas not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = request.data

        forum = Forum.objects.filter(id=int(serializer['forum'][0])).first()
        if forum:
            forum.last_message = server_now()
            forum.save(update_fields=['last_message'])

            return self.create(request, *args, **kwargs)
        else:
            return Response({'message': 'Forum doas not exist'}, status=status.HTTP_404_NOT_FOUND)
