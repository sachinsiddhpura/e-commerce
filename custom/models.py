from django.db import models

# Create your models here.
class Custom(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField()
	phone_number = models.IntegerField()
	second_phone_number = models.IntegerField()
	file 	=models.FileField(upload_to='photos/')

	def __str__(self):
		return self.name