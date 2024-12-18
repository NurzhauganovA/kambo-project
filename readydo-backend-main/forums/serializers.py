from rest_framework import serializers

from auth_user.models import User
from auth_user.serializers import UserModelSerializer
from common.serializers import BaseSerializer
from forums.models import Forum, Message


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        exclude = ('created_at', 'updated_at', 'grade')

    def to_representation(self, instance):
        data = super(ForumSerializer, self).to_representation(instance)
        data['username'] = instance.user.username
        data['grade'] = str(instance.user.grade)
        return data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        exclude = ('updated_at',)

    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        data['username'] = instance.auther.username
        return data
