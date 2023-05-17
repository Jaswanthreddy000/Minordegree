from django.db import models



# Create your models here.
class BTStudentInfo(models.Model):
   
    RegNo = models.IntegerField()
    RollNo = models.IntegerField()
    Name = models.CharField(max_length=255)
    Regulation = models.FloatField()
    Dept = models.IntegerField()
    AdmissionYear = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Category = models.CharField(max_length=30)
    GuardianName = models.CharField(max_length=255)
    Phone = models.TextField()
    email = models.TextField()
    Addressl = models.TextField()
    Address2 = models.TextField(null=True)


    class Meta:
        db_table = 'BTStudentInfo'
        constraints = [
            models.UniqueConstraint(fields=['RegNo'], name='unique BTStudentInfo_RegNo'),
            models.UniqueConstraint(fields=['RollNo'], name='unique BTStudentInfo_RollNo'),
        ]
        managed = True
