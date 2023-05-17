from django.db import models
import math
from ADAUGDB.models import BTRegistrationStatus
from django.db.models.signals import post_save
from django.dispatch import receiver

class BTMCourses(models.Model):
    SubCode = models.CharField(max_length=10)
    SubName = models.CharField(max_length=255)
    Credits = models.IntegerField()
    OfferedBy = models.IntegerField()
    CourseStructure = models.ForeignKey('BTMCourseStructure', on_delete=models.CASCADE)
    lectures = models.IntegerField()
    tutorials = models.IntegerField()
    practicals = models.IntegerField()
    DistributionRatio = models.TextField()
    MarkDistribution = models.ForeignKey('BTMMarksDistribution', on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'BTMCourses'
        constraints = [
            models.UniqueConstraint(fields=['SubCode', 'SubName', 'CourseStructure', 'DistributionRatio', 'MarkDistribution'], name='BTMCourses_unique_course')
        ]
        managed = True

class BTMMarksDistribution(models.Model):
    Regulation = models.FloatField()
    Distribution = models.TextField()
    DistributionNames = models.TextField()
    PromoteThreshold = models.TextField()
    
    class Meta:
        db_table = 'BTMMarksDistribution'
        unique_together = (('Regulation', 'Distribution', 'DistributionNames', 'PromoteThreshold'),)
        managed = True

    def __str__(self):
        return f"{self.Distribution}, {self.PromoteThreshold}"

    def distributions(self):
        distributions_names = self.DistributionNames.split(',')
        distributions_marks = self.Distribution.split(',')
        CHOICES = []
        outer_index = 0
        for names, marks in zip(distributions_names, distributions_marks):
            names = names.split('+')
            marks = marks.split('+')
            inner_index = 0
            for n, m in zip(names, marks):
                CHOICES += [(f"{outer_index}, {inner_index}", f"{n}, {m}")]
                inner_index += 1
            outer_index += 1
        return CHOICES

    def get_zeroes_string(self):
        distribution_marks = self.Distribution.split(',')
        marks = [row.split('+') for row in distribution_marks]
        zero_marks = [['0' for mark in range(len(row))] for row in marks]
        zero_marks = ['+'.join(mark) for mark in zero_marks]
        zeroes_string = ','.join(zero_marks)
        return zeroes_string 

    def get_marks_limit(self, outer, inner):
        return int(self.Distribution.split(',')[outer].split('+')[inner])

    def get_excel_column_index(self, outer, inner):
        distribution_marks = self.Distribution.split(',')
        marks = [row.split('+') for row in distribution_marks]
        index = 3  # index starts from 1 availing for the roll number (index=0) and name (index=1) rows in excel sheet.
        for num in range(outer):
            index += len(marks[num])
        index += inner
        return index



class BTMSubjectInfo(models.Model):
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
       db_table = 'BTMSubjectInfoV'
       managed = False

class BTMCourseStructure(models.Model):
    Byear = models.IntegerField()
    Bsem = models.IntegerField()
    Dept = models.IntegerField()
    Regulation = models.FloatField()
    Category = models.CharField(max_length=10)
    Type = models.CharField(max_length=10)
    Creditable = models.IntegerField()
    Credits = models.IntegerField()
    count = models.IntegerField()
    Rigid = models.BooleanField()
  

    class Meta:
        db_table = 'BTMCourseStructure'
        constraints = [
            models.UniqueConstraint(fields=['Category', 'Type' , 'Creditable', 'Credits', 'Regulation', 'Byear', 'Bsem', 'Dept'], name='Unique_BTMCourseStructureID')
        ]
        managed = True

class BTMSubjects(models.Model):
   RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', on_delete=models.CASCADE)
   course = models.ForeignKey('BTMCourses', on_delete=models.CASCADE, default=0)

   class Meta:
      db_table = 'BTMSubjects'
      unique_together = ('course', 'RegEventId')
      managed = True



class BTMStudentRegistrations(models.Model):
    student = models.ForeignKey('BTco_ordinator.BTRollLists', on_delete=models.CASCADE)
    RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', db_column='RegEventId', on_delete=models.CASCADE)
    Mode = models.IntegerField()
    sub_id = models.ForeignKey('BTMSubjects', db_column='sub_id', on_delete=models.CASCADE)
 

    class Meta:
        db_table = 'BTMStudentRegistrations'
        unique_together = (('student', 'RegEventId', 'sub_id'),)
        managed = True


class BTMMarks(models.Model):
    Registration = models.ForeignKey('BTMStudentRegistrations', on_delete=models.CASCADE)
    Marks = models.TextField()
    TotalMarks = models.IntegerField()
 

    class Meta:
        db_table = 'BTMMarks'
        constraints = [
            models.UniqueConstraint(fields=['Registration'], name='unique BTMmarks registration')
        ]
        managed = True

    def get_total_marks(self):
        marks_dis = self.Marks.split(',')
        marks_dis = [mark.split('+') for mark in marks_dis]
        subject = BTMSubjects.objects.filter(id=self.Registration.sub_id.id).first()
        
        ratio = subject.course.DistributionRatio

        if ':' not in ratio:
            ratio = f"{ratio}:1"
            marks_row = marks_dis[0]
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




class BTMStudentGrades(models.Model):
    RegId = models.ForeignKey('BTMStudentRegistrations', on_delete=models.CASCADE)
    RegEventId = models.IntegerField()
    Regulation = models.FloatField()
    Grade = models.CharField(max_length=2)
    AttGrade = models.CharField(max_length=2)
  

    class Meta:
        db_table = 'BTMStudentGrades'
        constraints = [
            models.UniqueConstraint(fields=['RegId'], name='unique BTMStudentGrades_registration')
        ]
        managed = True

class BTMGradesThreshold(models.Model):
    Grade = models.ForeignKey('BTMGradePoints', on_delete=models.CASCADE)
    Subject = models.ForeignKey('BTMSubjects', on_delete=models.CASCADE)
    RegEventId = models.ForeignKey('ADAUGDB.BTRegistrationStatus', on_delete=models.CASCADE)
    Threshold_Mark = models.FloatField()
    Section = models.CharField(max_length=2, default='NA')
    Exam_Mode = models.BooleanField() 
    
    class Meta:
        db_table = 'BTMGradesThreshold'
        unique_together = (('Grade', 'Subject', 'RegEventId', 'Section',"Exam_Mode"))
        managed = True

class BTMGradePoints(models.Model):
    Regulation = models.FloatField()
    Grade = models.CharField(max_length=2)
    Points = models.IntegerField()
    
    
    class Meta:
        db_table = 'BTMGradePoints'
        unique_together = (('Regulation', 'Grade', 'Points'))
        managed = True


class BTMStudentGradePoints(models.Model):
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
           db_table = 'BTMStudentGradePointsMV'
           managed = False



