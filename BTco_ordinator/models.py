from django.db import models
from ADAUGDB.models import BTRegistrationStatus
from ADAUGDB.models import BTCourses

from BTExamStaffDB.models import BTStudentInfo

# Create your models here.

class BTStudentGradePoints(models.Model):
     RegNo = models.IntegerField()
     sub_id = models.IntegerField()
     SubCode = models.CharField(max_length=10)
     SubName = models.CharField(max_length=100)
     CourseStructure_id = models.IntegerField()
     AYear = models.IntegerField()
     ASem = models.IntegerField()
     BYear = models.IntegerField()
     BSem = models.IntegerField()
     OfferedYear = models.IntegerField()
     Dept = models.IntegerField() 
     Grade = models.CharField(max_length=2)
     AttGrade = models.CharField(max_length=2)
     Regulation = models.FloatField()
     Creditable = models.IntegerField()  
     Credits = models.IntegerField()
     Course_Credits = models.IntegerField()
     Type = models.CharField(max_length=10)
     Category = models.CharField(max_length=10)
     Points = models.IntegerField() 
     GP = models.IntegerField() 
     AYASBYBS = models.IntegerField()
     class Meta:
        db_table = 'BTStudentGradePointsMV'
        managed = False


class BTSubjectInfo(models.Model):
   AYear = models.IntegerField()
   ASem = models.IntegerField()
   BYear = models.IntegerField()
   BSem = models.IntegerField()
   Regulation = models.FloatField()
   Mode = models.CharField(max_length=1)
   Dept = models.IntegerField()
   SubId = models.IntegerField()
   SubCode = models.CharField(max_length=10)
   SubName = models.CharField(max_length=100)
   Credits = models.IntegerField()
   OfferedBy = models.IntegerField()
   Type = models.CharField(max_length=10)
   Category = models.CharField(max_length=10)
   DistributionRatio = models.TextField()
   Distribution = models.TextField()
   DistributionNames = models.TextField()
   PromoteThreshold = models.TextField()
   class Meta:
       db_table = 'BTSubjectInfoV'
       managed = False



class BTRollLists(models.Model):
    student = models.ForeignKey('BTExamStaffDB.BTStudentInfo', on_delete=models.CASCADE)
    RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', on_delete=models.CASCADE)
    Section = models.CharField(max_length=2, default='NA')
   
    class Meta:
       db_table = 'BTRollLists'
       unique_together = ('student', 'RegEventId')
       managed = True


class BTSubjects(models.Model):
   RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', on_delete=models.CASCADE)
   course = models.ForeignKey('ADAUGDB.BTCourses', on_delete=models.CASCADE, default=0)

   class Meta:
      db_table = 'BTSubjects'
      unique_together = ('course', 'RegEventId')
      managed = True



class BTStudentRegistrations(models.Model):
    student = models.ForeignKey('BTco_ordinator.BTRollLists', on_delete=models.CASCADE)
    RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', db_column='RegEventId', on_delete=models.CASCADE)
    Mode = models.IntegerField()
    sub_id = models.ForeignKey('BTco_ordinator.BTSubjects', db_column='sub_id', on_delete=models.CASCADE)
 

    class Meta:
        db_table = 'BTStudentRegistrations'
        unique_together = (('student', 'RegEventId', 'sub_id'),)
        managed = True




