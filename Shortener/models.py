from django.db import models

class ShortLink(models.Model):
    code = models.CharField(max_length=16,unique=True,db_index=True)
    long_url = models.URLField(max_length=2000)
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default= True)


class ClickEvent(models.Model):
    link = models.ForeignKey(ShortLink,on_delete=models.CASCADE, related_name = 'clicks')
    ts = models.DateTimeField(auto_now_add=True,db_index=True)
    ip_hash = models.CharField(max_length=64 ,blank=True)
    user_agent = models.TextField(blank=True)
    referer = models.TextField(blank=True)

    
