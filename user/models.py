from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле электронной почты должно быть задано')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Institution(models.Model):
    name = models.CharField(max_length=100, verbose_name="Учреждение")
    fullname = models.CharField(max_length=200, verbose_name="Полное название учреждения")

    class Meta:
        verbose_name = "учреждение"
        verbose_name_plural = "Учреждения"

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Группа")
    fullname = models.CharField(max_length=100, verbose_name="Полное название группы")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Учреждение")

    class Meta:
        verbose_name = "группу"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"{self.fullname}"


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=30, verbose_name="Отчество", blank=True)
    group_student = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа", related_name='profile_groups', null=True, blank=True)
    year_of_admission = models.PositiveIntegerField(verbose_name="Год поступления", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"


    def get_current_course(self):
        if not self.year_of_admission:
            return None
        current_date = timezone.now()
        current_year = current_date.year
        current_month = current_date.month
        
        # Если месяц до сентября (включительно), уменьшить на один учебный год
        if current_month < 9:
            current_year -= 1
        
        return current_year - self.year_of_admission + 1
