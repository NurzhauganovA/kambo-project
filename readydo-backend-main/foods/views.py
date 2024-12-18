from unicodedata import decimal

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from auth_user.models import User
from auth_user.serializers import UserModelSerializer, UserProfileSerializer
from common.manual_parameters import CUISINE_TYPES_ARRAY, TASTE_TYPES_ARRAY, START_PRICE, END_PRICE, BEST_FOODS, \
    FOOD_ID, USER_ID
from foods.models import Food, Favorites, EstimationTypes, Estimation
from foods.serializers import FoodSerializer, FavoritesSerializer, EstimationSerializer
from foods.services import recalculate_grade


class FoodsApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = FoodSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'cuisine', 'taste')

    def get_queryset(self):
        cuisine_types = self.request.query_params.get('cuisine_ids')
        taste_types = self.request.query_params.get('taste_ids')
        start_price = self.request.query_params.get('start_price')
        end_price = self.request.query_params.get('end_price')
        best_foods = self.request.query_params.get('best_foods')
        user_id = self.request.query_params.get('user_id')

        foods = Food.objects.all()
        if best_foods is None:
            if cuisine_types:
                status_nums = [int(sid) for sid in cuisine_types.split(',')]
                foods = foods.filter(cuisine__in=status_nums)
            if taste_types:
                status_nums = [int(sid) for sid in taste_types.split(',')]
                foods = foods.filter(taste__in=status_nums)
            if start_price:
                foods = foods.filter(price__gt=start_price)
            if end_price:
                foods = foods.filter(price__lt=end_price)
        elif best_foods == 1:
            foods = foods.order_by('-user__grade')
        elif best_foods == 2:
            foods = foods.order_by('-grade')
        if user_id:
            foods = foods.filter(user__id=user_id)

        return foods

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(manual_parameters=[CUISINE_TYPES_ARRAY, TASTE_TYPES_ARRAY, START_PRICE, END_PRICE, BEST_FOODS, USER_ID])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FoodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Food.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = FoodSerializer

    def put(self, request, *args, **kwargs):
        permission = Food.objects.filter(user=self.request.user)
        if permission:
            return self.update(request, *args, **kwargs)
        return Response({'message': 'У вас нет прав для редактирования'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        permission = Food.objects.filter(user=self.request.user)
        if permission:
            return self.partial_update(request, *args, **kwargs)
        return Response({'message': 'У вас нет прав для редактирования'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        permission = Food.objects.filter(user=self.request.user)
        if permission:
            return self.destroy(request, *args, **kwargs)
        return Response({'message': 'У вас нет прав для удаления'}, status=status.HTTP_403_FORBIDDEN)


class FavoritesViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        user = self.request.user
        return Favorites.objects.filter(user=user)


class FavoritesOptionViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request, pk):
        user = self.request.user
        food = Food.objects.filter(id=pk).first()
        if food:
            favorites = Favorites.objects.filter(user=user, food__id=pk).first()
            if favorites:
                favorites.delete()
                return Response({'message': 'delete'}, status=status.HTTP_204_NO_CONTENT)
            Favorites.objects.create(user=user, food=food)
            return Response({'message': 'create'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Food doas not exist'})


class EstimationViewSet(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = EstimationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        if self.request.user.id != int(data['user']):
            return Response({'message': 'Ведите свой id'}, status=status.HTTP_403_FORBIDDEN)
        if (1 <= int(data['grade']) <= 5) is False:
            return Response({'message': 'grade is min. 1, max. 5'}, status=status.HTTP_400_BAD_REQUEST)

        if data['type'] == '1':
            if User.objects.filter(id=int(data['value_id'])).exists() is False:
                return Response({'message': 'Chef doas not exists'}, status=status.HTTP_404_NOT_FOUND)
            Estimation.objects.create(user=self.request.user, grade=decimal(data['grade']), type=EstimationTypes.CHEF,
                                      value_id=int(data['value_id']))

        if data['type'] == '2':
            if Food.objects.filter(id=int(data['value_id'])).exists() is False:
                return Response({'message': 'Food doas not exists'}, status=status.HTTP_404_NOT_FOUND)
            Estimation.objects.create(user=self.request.user, grade=decimal(data['grade']), type=EstimationTypes.FOOD,
                                      value_id=int(data['value_id']))

        recalculate_grade(int(data['type']), int(data['value_id']))

        return Response({'message': 'create'}, status=status.HTTP_201_CREATED)


class BestChefsViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.all().order_by('-grade')
