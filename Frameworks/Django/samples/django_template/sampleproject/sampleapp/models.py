from django.conf import settings
from django.db import models


class Sample(models.Model):
    title = models.CharField('タイトル', max_length=128)
    text = models.TextField('テキスト', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='登録者', on_delete=models.CASCADE)
    created_at = models.DateTimeField('登録日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)


    def __str__(self):
        return self.title
