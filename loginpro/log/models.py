from djongo import models

# Create your models here.

class StudentMarks(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.TextField(max_length=30)
    marks = models.TextField(max_length=5)
    