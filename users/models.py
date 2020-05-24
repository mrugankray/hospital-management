from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prof = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor')
    )
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    prof = models.CharField(max_length=20, choices=prof, default='Patient')
    gender = models.CharField(max_length=20, choices=gender, default='Male')
    age = models.CharField(max_length=4, default='Null')
    bloodGroup = models.CharField(max_length=4, default='Null')
    phoneNumber = models.CharField(max_length=10, default='Null')
    casePaper = models.CharField(max_length=100, default='Null')

    def __str__(self):
        return f"{self.user.username} Profile"


class Prescription(models.Model):
    doc_name = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=100)
    prescription = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    patient_fullname = models.CharField(max_length=50, default='default')
    patient_username = models.CharField(max_length=50, default='default')

    def __str__(self):
        return str(self.patient_username)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
