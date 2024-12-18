from rest_framework import serializers

from auth_user.models import User
from auth_user.serializers import UserModelSerializer, UserProfileSerializer
from foods.models import Food, Favorites, Estimation


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'

    def to_representation(self, instance):
        data = super(FoodSerializer, self).to_representation(instance)
        data['username'] = instance.user.username
        data['is_favorite'] = Favorites.objects.filter(user=instance.user, food=instance).exists()
        return data


class FavoritesSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    food = FoodSerializer()

    class Meta:
        model = Favorites
        exclude = ('created_at', 'updated_at')


class EstimationSerializer(serializers.ModelSerializer):
    grade = serializers.IntegerField()

    class Meta:
        model = Estimation
        exclude = ('created_at', 'updated_at')

        extra_kwargs = {'type': {'help_text': 'CHEF = 1, FOOD = 2'},
                        'value_id': {'help_text': 'id chef or food', 'required': True},
                        'grade': {'help_text': 'max. number 5'}}
