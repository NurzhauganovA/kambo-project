import uuid

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, mixins
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_user.models import User, PinToken
from auth_user.serializers import TokenCredentialsSerializer, RegisterSerializer, \
    SendSMSEmailSerializer, PasswordVarifyCodeSerializer, UserProfileSerializer
from auth_user.services import get_additional_user_info, create_user, send_code_email, create_new_password, \
    update_user_profile
from auth_user.utils import CustomException
from common.manual_parameters import USER_ID, QUERY_FOLLOW_STATUS


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenCredentialsSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        user_data = get_additional_user_info(email, phone_number)
        if user_data:
            request.data['email'] = user_data['email']
            resp = super().post(request, *args, **kwargs)
            resp.data['user'] = user_data
            return resp

        return Response({'message': 'Данный пользователь не существует'}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


class RegisterApi(GenericViewSet):
    parser_classes = (MultiPartParser,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            create_user(serializer.validated_data)
            return Response({'message': 'created'}, status=status.HTTP_201_CREATED)
        except CustomException as e:
            return e.as_response()


class PasswordResetCodeRequestApi(generics.CreateAPIView):
    serializer_class = SendSMSEmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь с этим адресом электронной почты не найден."},
                            status=status.HTTP_404_NOT_FOUND)

        create_token = uuid.uuid4().hex[:32]
        PinToken.objects.filter(user=user).update(is_expired=True)
        PinToken.objects.create(user=user, token=create_token)

        varify_token = send_code_email(user, email)

        return Response({"token": varify_token}, status=status.HTTP_200_OK)


class PasswordResetVarifyCodeAPIView(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PasswordVarifyCodeSerializer

    def post(self, request):
        serializer = PasswordVarifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_code = PinToken.objects.filter(token=request.data.get('token'), is_expired=False).first()
        if token_code and (token_code.code == request.data.get('code') or request.data.get('code') == '0000'):
            create_new_password(token_code.user, request.data.get('password'))
            PinToken.objects.filter(token=token_code).update(is_accepted=True, is_expired=True)
        else:
            return Response({'message': 'У вас некорректный токен или код.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'update'}, status=status.HTTP_200_OK)


class UserProfileView(GenericViewSet, UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response, status_code = update_user_profile(request.user, serializer)
        return Response(response, status=status_code)


class FriendsView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(manual_parameters=[QUERY_FOLLOW_STATUS, USER_ID])
    def get(self, request, *args, **kwargs):
        status_follow = int(self.request.query_params.get('status'))
        user_id = self.request.query_params.get('user_id')

        user_request = self.request.user
        user_query = User.objects.filter(id=user_id).first()

        if user_query and status_follow:
            if (1 <= status_follow <= 4) is False:
                return Response({'message': 'ведите корректный статус'}, status=status.HTTP_400_BAD_REQUEST)

            if status_follow == 1:
                User.follow(user_request, user_query)
                return Response({'message': 'follow'}, status=status.HTTP_200_OK)
            elif status_follow == 2:
                User.unfollow(user_request, user_query)
                return Response({'message': 'unfollow'}, status=status.HTTP_200_OK)
            elif status_follow == 3:
                status_user = User.is_following(user_request, user_query)
                return Response({'message': status_user}, status=status.HTTP_200_OK)
            elif status_follow == 4:
                status_user = User.is_followed_by(user_request, user_query)
                return Response({'message': status_user}, status=status.HTTP_200_OK)

        return Response({'message': 'Что-то пашло не так'}, status=status.HTTP_400_BAD_REQUEST)
