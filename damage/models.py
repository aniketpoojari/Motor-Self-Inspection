from django.db import models

# Create your models here.
class Claims(models.Model):
	userid = models.CharField(max_length = 50)
	claimno = models.PositiveIntegerField()
	description = models.CharField(max_length = 1000)
	status = models.PositiveSmallIntegerField()
	date = models.DateTimeField(auto_now_add = True)
