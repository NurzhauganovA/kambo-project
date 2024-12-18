from django.db import models
from django.db.models import CASCADE
from imagekit import processors
from imagekit.models import ProcessedImageField

from auth_user.models import User
from common.models import BaseModel


class Forum(BaseModel):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    name = models.CharField(blank=True)
    photo = ProcessedImageField(
        upload_to='forums/',
        processors=[processors.Transpose()],
        options={'quality': 60},
        null=True,
        blank=True
    )
    description = models.TextField(blank=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    last_message = models.DateTimeField(null=True)


class Message(BaseModel):
    forum = models.ForeignKey(Forum, on_delete=CASCADE, null=False)
    auther = models.ForeignKey(User, on_delete=CASCADE, null=False)
    message = models.TextField(blank=True)
