from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


media_url=settings.MEDIA_URL



class new_request(models.Model):
    title = models.CharField(max_length=1000,blank=True,default=None)
    creator = models.CharField(max_length=1000,blank=True,default=None)
    department = models.CharField(max_length=1000,blank=True,default=None)
    status = models.CharField(max_length=1000,blank=True,default=None)
    priority = models.CharField(max_length=1000,blank=True,default=None)
    severity = models.CharField(max_length=1000,blank=True,default=None)
    creation_date = models.CharField(max_length=1000,blank=True,default=None)
    last_modified_date = models.CharField(max_length=5000,blank=True,default=None)
    description = models.CharField(max_length=5000,blank=True,default=None)
    primary_assignee = models.CharField(max_length=1000,blank=True,default=None)
    

    
class request_attachment(models.Model):
    new_request = models.ForeignKey( new_request )
    attachment1 = models.FileField(upload_to='attachment', blank=True)
    attachment2 = models.FileField(upload_to='attachment', blank=True)
    attachment3 = models.FileField(upload_to='attachment', blank=True)
    attachment4 = models.FileField(upload_to='attachment', blank=True)
    attachment5 = models.FileField(upload_to='attachment', blank=True)
    attachment6 = models.FileField(upload_to='attachment', blank=True)
    attachment7 = models.FileField(upload_to='attachment', blank=True)
    attachment8 = models.FileField(upload_to='attachment', blank=True)
    attachment9 = models.FileField(upload_to='attachment', blank=True)
    attachment10 = models.FileField(upload_to='attachment', blank=True)
    
 
class request_owners(models.Model):
    new_request = models.ForeignKey( new_request )
    request_owner = models.CharField(max_length=1000,blank=True,default=None)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department=models.CharField(max_length=40,null=True,default='None')
    admin=models.CharField(max_length=40,null=True,default='None')
    def __str__(self):  
        return "%s's profile" % self.user 
    
    def save(self, *args, **kwargs):
        try:
            existing = UserProfile.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except UserProfile.DoesNotExist:
            pass 
        models.Model.save(self, *args, **kwargs)
        
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User) 
    
