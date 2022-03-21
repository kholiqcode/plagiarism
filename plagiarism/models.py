from enum import Enum
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.forms import model_to_dict

# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username,email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if username is None:
            raise TypeError('Users must have a username.')

        if not email:
            raise ValueError('The Email must be set')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,unique=True)
    username = models.CharField(max_length=50,null=True,unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    class Meta:
        db_table = 'users'

    def to_dict(self):
        user_dict = model_to_dict(self)
        del user_dict['password']
        return user_dict

class Golongan(models.Model):
    nama = models.CharField(max_length=10,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'golongan'

class Semester(Enum):

    SATU = 1
    DUA = 2
    TIGA = 3
    EMPAT = 4
    LIMA = 5
    ENAM = 6
    TUJUH = 7
    DELAPAN = 8

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class MataKuliah(models.Model):
    nama = models.CharField(max_length=100,null=True)
    semester = models.SmallIntegerField(null=True, choices=Semester.choices(),default=Semester.SATU)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'mata_kuliah'

class LearningJurnal(models.Model):
    email = models.CharField(max_length=100,null=True)
    nama = models.CharField(max_length=100,null=True)
    nim = models.CharField(max_length=10,null=True)
    semester = models.SmallIntegerField(null=True, choices=Semester.choices(),default=Semester.SATU)
    golongan = models.CharField(max_length=2,null=True)
    matkul = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, null=True)
    minggu = models.SmallIntegerField(null=True)
    tanggal_perkuliahan = models.DateField(null=True)
    topik = models.CharField(max_length=255,null=True)
    pembahasan = models.TextField(null=True)
    cleaning = models.TextField(null=True)
    casefolding = models.TextField(null=True)
    tokenizing = models.TextField(null=True)
    normalisasi = models.TextField(null=True)
    stopword = models.TextField(null=True)
    steeming = models.TextField(null=True)
    cleaned = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'learning_jurnal'

class JurnalSimilarity(models.Model):
    doc1 = models.ForeignKey(LearningJurnal, on_delete=models.CASCADE, null=True,related_name="fn_lj_doc1")
    doc2 = models.ForeignKey(LearningJurnal, on_delete=models.CASCADE, null=True,related_name="fn_lj_doc2")
    score = models.FloatField(null=True)
    score_percentage = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'jurnal_similarity'