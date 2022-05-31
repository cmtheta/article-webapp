from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='name', on_delete=models.PROTECT) 
    title = models.CharField(verbose_name='タイトル', max_length=100)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo = models.ImageField(verbose_name='画像', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='post_time', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='update_time', auto_now=True)

    class Meta:
        verbose_name_plural = 'Article'
    
    def __str__(self):
        return self.title