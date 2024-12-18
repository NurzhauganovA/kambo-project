from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ошибка'
    default_code = 'unknown'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.status_code = kwargs.get('status_code') or self.status_code
        self.default_detail = kwargs.get('default_detail') or self.default_detail
        self.default_code = kwargs.get('default_code') or self.default_code

    def as_response(self) -> Response:
        return Response(
            {'message': self.default_detail, 'code': self.default_code},
            self.status_code,
        )


class PhoneNumberExistsException(CustomException):
    status_code = status.HTTP_423_LOCKED
    default_detail = 'Этот номер телефона уже существует'
    default_code = 'phone-number-exists'


class EmailExistsException(CustomException):
    status_code = status.HTTP_423_LOCKED
    default_detail = 'Уже есть пользователь с такой почтой'
    default_code = 'email-exists'
