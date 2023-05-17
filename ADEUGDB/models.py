from django.db import models
from ADAUGDB.models import BTGradePoints
from ADAUGDB.models import BTRegistrationStatus
from BTco_ordinator.models import BTSubjects

# Create your models here.

class BTGradesThreshold(models.Model):
    Grade = models.ForeignKey('ADAUGDB.BTGradePoints', on_delete=models.CASCADE)
    Subject = models.ForeignKey('BTco_ordinator.BTSubjects', on_delete=models.CASCADE)
    RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', on_delete=models.CASCADE)
    Threshold_Mark = models.FloatField()
    Section = models.CharField(max_length=2, default='NA')
    Exam_Mode = models.BooleanField() 
    
    class Meta:
        db_table = 'BTGradesThreshold'
        unique_together = (('Grade', 'Subject', 'RegEventId', 'Section',"Exam_Mode"))
        managed = True