from django.db import models
from BTco_ordinator.models import BTStudentRegistrations
from BTco_ordinator.models import BTSubjects
import math
# Create your models here.
class BTMarks(models.Model):
    Registration = models.ForeignKey('BTco_ordinator.BTStudentRegistrations', on_delete=models.CASCADE)
    Marks = models.TextField()
    TotalMarks = models.IntegerField()
 

    class Meta:
        db_table = 'BTMarks'
        constraints = [
            models.UniqueConstraint(fields=['Registration'], name='unique BTmarks registration')
        ]
        managed = True

    def get_total_marks(self):
        marks_dis = self.Marks.split(',')
        marks_dis = [mark.split('+') for mark in marks_dis]
        subject = BTSubjects.objects.filter(id=self.Registration.sub_id.id).first()
        
        ratio = subject.course.DistributionRatio

        if ':' not in ratio:
            ratio = f"{ratio}:1"
            sub_total = 0
            for mark in marks_row:
                sub_total += float(mark)
            return sub_total

        else:
            ratio = ratio.split(':')
            total_parts = 0
            for part in ratio:
                total_parts += int(part)
            total = 0
            for index in range(len(marks_dis)):
                marks_row = marks_dis[index]
                sub_total = 0
                for mark in marks_row:
                    sub_total += float(mark)
                    total += sub_total*int(ratio[index])
            return math.ceil(total/total_parts)


class BTStudentGrades(models.Model):
    RegId = models.ForeignKey('BTco_ordinator.BTStudentRegistrations', db_column="RegId", on_delete=models.CASCADE)
    RegEventId = models.IntegerField()
    Regulation = models.FloatField()
    Grade = models.CharField(max_length=2)
    AttGrade = models.CharField(max_length=2)
  

    class Meta:
        db_table = 'BTStudentGrades'
        constraints = [
            models.UniqueConstraint(fields=['RegId'], name='unique BTStudentGrades_registration')
        ]
        managed = True