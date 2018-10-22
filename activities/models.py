from django.db import models
from django.utils import timezone
from accounts.models import User



class Groups(models.Model):
    group_name = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(default=timezone.now)
    mod_time = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='avatar')
    logo = models.ImageField(upload_to='logo')
    has_confirmed = models.BooleanField(default=False)
    permitted = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ['-c_time']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Activities(models.Model):
    group_name = models.ForeignKey(Groups, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=20)
    links = models.CharField(max_length=200)
    img = models.ImageField(upload_to='img')
    pub_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(auto_now=True)
    begin = models.DateTimeField('start date')
    end = models.DateTimeField(default=timezone.now)
    desc = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    interval = models.BooleanField(default=False)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ["-begin", "-pub_date"]
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'


class GroupConfirmString(models.Model):
    code = models.CharField(max_length=256)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    c_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.group.group_name + ':   ' + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = 'confirmation code'
        verbose_name_plural = 'confirmation codes'

