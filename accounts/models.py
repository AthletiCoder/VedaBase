from django.db import models
from django.contrib.auth.models import AbstractUser
  
# Create your models here.
class Account(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'user'),
      (2, 'tagger'),
      (3, 'reviewer'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

class Session(models.Model):
    session_id = models.CharField(max_length=32, unique=True)

class UserSession(Session):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user_session')