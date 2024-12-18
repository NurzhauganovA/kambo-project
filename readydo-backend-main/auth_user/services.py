from typing import Optional

from django.contrib.auth.hashers import make_password

from auth_user.models import User, PinToken
from auth_user.serializers import UserModelSerializer
from auth_user.utils import PhoneNumberExistsException, EmailExistsException


def get_additional_user_info(email: str, phone_number: str) -> Optional[dict]:
    user = User.objects.filter(email=email).first() if email else None
    if not user:
        user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        return None

    user_data = UserModelSerializer(user).data

    return user_data


def create_user(validated_data: dict) -> User:
    if User.objects.filter(phone_number=validated_data['phone_number']).exists():
        raise PhoneNumberExistsException()

    if User.objects.filter(email__iexact=validated_data['email']).exists():
        raise EmailExistsException()

    user = User()
    user.email = validated_data['email']
    user.first_name = validated_data['first_name']
    user.last_name = validated_data['last_name']
    user.middle_name = validated_data['middle_name']
    user.phone_number = validated_data['phone_number']
    user.username = validated_data['username']
    user.address = validated_data['address']
    user.about_yourself = validated_data['about_yourself']
    user.pending_password = validated_data['password']
    user.password = make_password(validated_data['password'])
    user.avatar = validated_data.get('avatar')
    user.save()

    return user


def send_code_email(user, email):
    pin_code = PinToken.objects.filter(user=user).order_by('-created_at').first()
    code = pin_code.code
    token = pin_code.token

    print(code)

    # NEED CREATE LOGIC SEND SMS TO EMAIL
    # sender_email = 'ndusenbai@gmail.com'
    # recipient_email = email
    # app_password = 'bfkgconnttaxxhqk'
    #
    # # Создание сообщения
    # message = MIMEMultipart()
    # message["From"] = sender_email
    # message["To"] = recipient_email
    # message["Subject"] = "Reset Password "
    # message.attach(MIMEText(str(user)))
    #
    # # Подключение к SMTP-серверу Gmail
    # with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #     server.starttls()
    #
    #     # Вход с использованием App Password
    #     server.login(sender_email, app_password)
    #
    #     # Отправка письма
    #     server.sendmail(sender_email, recipient_email, message.as_string())

    return token


def create_new_password(user, password):
    User.objects.filter(email=user.email).update(password=make_password(password))


def update_user_profile(user, serializer):
    data = serializer.validated_data
    serializer = UserModelSerializer(user, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data, 200
