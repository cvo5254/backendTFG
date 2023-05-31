from django.db import models
from channels.models import Channel
from users.models import CustomUser

class Emergency(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    report_date = models.DateTimeField()
    publish_date = models.DateTimeField(blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    images = models.ImageField(upload_to='emergency_images/', blank=True, null=True)

