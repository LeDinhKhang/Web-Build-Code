from django.db.models.fields import TextField
from djongo import models

# Create your models here.
class BaiTap(models.Model):
    id_bai = models.CharField(max_length=5)
    debai = models.TextField()
    dapan = models.TextField()


