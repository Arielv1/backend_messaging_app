from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.CharField(max_length=200, null=False)
    receiver = models.CharField(max_length=200, null=False)
    subject = models.CharField(max_length=200, null=False)
    message = models.CharField(max_length=200, null=False)
    was_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.message_id, self.sender, self.receiver, self.message, self.subject, self.date_created, self.was_read}'

    class Meta:
        db_table = 'db_messages'
