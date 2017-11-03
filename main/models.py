from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#line => user 外键
class line(models.Model):
    num = models.CharField(max_length=10,unique=True)
    # line = models.ForeignKey(to='Profile',to_field='user')
    line = models.ManyToManyField('Profile',symmetrical=False)
    def __str__(self):
        return self.num

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # password = models.OneToOneField(password,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create your models here.
