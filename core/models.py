from django.db import models
import uuid


class VPS(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='uid ')
    cpu = models.PositiveIntegerField(verbose_name='')
    ram = models.PositiveIntegerField(verbose_name='')
    hdd = models.PositiveIntegerField(verbose_name='')
    status = models.CharField(max_length=20, choices=[
        ('started', 'Started'),
        ('blocked', 'Blocked'),
        ('stopped', 'Stopped'),
    ], default='started', verbose_name='Статус облачного сервера')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания настройки облачного сервера')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления настройки облачного сервера')

    def __str__(self):
        return str(self.uid)
