import uuid
from random import randint

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from datetime import date


class UserProfileManager(BaseUserManager):
    def create_user(self, phone, birth_date, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, birth_date=birth_date, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, birth_date, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, birth_date, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='userprofile_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='userprofile_permissions', blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['birth_date']

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.phone


class Order(models.Model):
    order_number = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    attachments = models.ManyToManyField('Attachment', blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            number = uuid.uuid4().int
            number %= 1000000
            self.order_number = str(number).zfill(6)
        super(Order, self).save(*args, **kwargs)


class Attachment(models.Model):
    file = models.FileField(upload_to='orders/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
