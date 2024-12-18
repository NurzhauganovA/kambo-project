import random
from datetime import datetime, timedelta

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CASCADE
from imagekit import processors
from imagekit.models import ProcessedImageField

from common.dates import server_now
from common.models import BaseModel


class Grade(models.IntegerChoices):
    BAD = 1, 'bad'
    SATISFACTORY = 2, 'satisfactory'
    NORMAL = 3, 'normal'
    GOOD = 4, 'good'
    GREAT = 5, 'great'

    @staticmethod
    def get_status(status):
        if status == Grade.BAD:
            return 'bad'
        elif status == Grade.SATISFACTORY:
            return 'satisfactory'
        elif status == Grade.NORMAL:
            return 'normal'
        elif status == Grade.GOOD:
            return 'good'
        elif status == Grade.GREAT:
            return 'Great'


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=70, unique=True)
    username = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=False)
    avatar = ProcessedImageField(
        upload_to='avatar/',
        processors=[processors.Transpose()],  # transpose - to fix the 90˚ rotation issue
        options={'quality': 60},
        null=True,
        blank=True
    )
    grade = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    address = models.CharField(max_length=250, blank=True)
    about_yourself = models.TextField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    language = models.CharField(max_length=10, default='ru')
    created_at = models.DateTimeField(auto_now=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def follow(self, user):
        """Подписаться на пользователя."""
        if user not in self.following.all():
            self.following.add(user)

    def unfollow(self, user):
        """Отписаться от пользователя."""
        if user in self.following.all():
            self.following.remove(user)

    def is_following(self, user):
        """Проверить, подписан ли текущий пользователь на данного пользователя."""
        return user in self.following.all()

    def is_followed_by(self, user):
        """Проверить, подписан ли данный пользователь на текущего пользователя."""
        return self in user.following.all()

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PinToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pin_codes')
    code = models.CharField(max_length=4, blank=True)
    token = models.CharField(max_length=32, blank=True)
    expiration = models.DateTimeField(blank=True, editable=False)
    is_accepted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, Code: {self.code}, Accepted: {self.is_accepted}"

    def set_accept_code(self):
        self.code = str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        if not self.code:
            self.expiration = server_now() + timedelta(days=1)
            self.set_accept_code()
        super(PinToken, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['code', 'is_accepted']
        verbose_name = "Код для восстановления пароля"
        verbose_name_plural = "Коды для восстановления пароля"
