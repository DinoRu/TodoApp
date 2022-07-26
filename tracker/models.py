from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
	name = models.CharField(max_length=250)
	description = models.TextField()
	created_date = models.DateField(auto_now_add=True)
	due_date = models.DateField()
	schedule_date = models.DateField()
	closed = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


	def __str__(self):
		return self.name

	class Meta:
		ordering = ['created_date']
		


