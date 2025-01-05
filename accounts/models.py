from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.generate_code import generate_code
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    code = models.CharField(max_length=10, default=generate_code)
    first_name = models.CharField(max_length=15, null=True, blank=True)
    last_name = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)  # New field for shipping address
    date_of_birth = models.DateField(null=True, blank=True)  # Optional field for date of birth
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True, blank=True)  # Gender field
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # Payment method preference (e.g., Credit Card, PayPal)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created :
        Profile.objects.create(
            user = instance
        )




ADDRESS_TYPES = (
    ('Home','Home'),
    ('Business','Business'),
    ('Office','Office'),
    ('Academy','Academy'),
    ('Other','Other'),
)

class Address(models.Model):
    user = models.ForeignKey(User,related_name='user_address', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address = models.TextField(max_length=300)
    notes = models.TextField(null=True,blank=True)



PHONE_TYPES = (
    ('Primary','Primary'),
    ('Secondary','Secondary'),
)

class Phone(models.Model):
    user = models.ForeignKey(User,related_name='user_phone', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=PHONE_TYPES)
    phone = models.CharField(max_length=25)