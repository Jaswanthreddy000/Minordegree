from django.db import models



# Create your models here.
class BTRegistrationStatus(models.Model):
    AYear = models.IntegerField()
    ASem = models.IntegerField()
    BYear = models.IntegerField()
    BSem = models.IntegerField()
    Regulation = models.FloatField()
    Dept = models.IntegerField()
    Mode = models.CharField(max_length=1) # R for Regular B for Backlog
    Status = models.IntegerField()
    RollListStatus = models.IntegerField()
    RollListFeeStatus = models.IntegerField()
    OERollListStatus = models.IntegerField()
    OERegistrationStatus = models.IntegerField()
    RegistrationStatus = models.IntegerField()
    MarksStatus = models.IntegerField()
    GradeStatus = models.IntegerField()
 

    class Meta:
        db_table = 'BTRegistration_Status'
        constraints = [
            models.UniqueConstraint(fields=['AYear', 'ASem', 'BYear', 'BSem', 'Regulation', 'Dept', 'Mode'], name="unique_BTRegistrationstatus")
        ]
        managed = True

    def __str__(self):
        name = str(DEPARTMENTS[self.Dept-1]) + ':' + str(YEARS[self.BYear]) + ':' + str(SEMS[self.BSem]) + ':' + \
            str(self.AYear) + ':' + str(self.ASem) + ':' + str(self.Regulation) + ':' + str(self.Mode)
        return name

    def __repr__(self):
        name = str(YEARS[self.BYear]) + ':' + str(SEMS[self.BSem]) + ':' + \
            str(self.AYear) + ':' + str(self.ASem) + ':' + str(self.Regulation) + ':' + str(self.Mode)
        return name
DEPARTMENTS = {
    1: "Computer Science",
    2: "Electronics and Communication Engineering",
    3: "Electrical and Electronics Engineering",
    4: "Mechanical Engineering",
    5: "Civil Engineering",
    6: "Chemical Engineering",
    7: "Biotechnological Engineering",
    8: "Materials and Metallurgical Engineering"
}

SEMS = {
    1: "I",
    2: "II",
}

YEARS = {
    1: "First Year",
    2: "Second Year",
    3: "Third Year",
    4: "Fourth Year",
}


    
class BTCourses(models.Model):
    SubCode = models.CharField(max_length=10)
    SubName = models.CharField(max_length=255)
    Credits = models.IntegerField()
    OfferedBy = models.IntegerField()
    CourseStructure = models.ForeignKey('BTCourseStructure', on_delete=models.CASCADE)
    lectures = models.IntegerField()
    tutorials = models.IntegerField()
    practicals = models.IntegerField()
    DistributionRatio = models.TextField()
    MarkDistribution = models.ForeignKey('BTMarksDistribution', on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'BTCourses'
        constraints = [
            models.UniqueConstraint(fields=['SubCode', 'SubName', 'CourseStructure', 'DistributionRatio', 'MarkDistribution'], name='BTCourses_unique_course')
        ]
        managed = True



class BTMarksDistribution(models.Model):
    Regulation = models.FloatField()
    Distribution = models.TextField()
    DistributionNames = models.TextField()
    PromoteThreshold = models.TextField()
  

    class Meta:
        db_table = 'BTMarksDistribution'
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

class BTCourseStructure(models.Model):
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
        db_table = 'BTCourseStructure'
        constraints = [
            models.UniqueConstraint(fields=['Category', 'Type' , 'Creditable', 'Credits', 'Regulation', 'Byear', 'Bsem', 'Dept'], name='Unique_BTCourseStructureID')
        ]
        managed = True


class BTGradePoints(models.Model):
    Regulation = models.FloatField()
    Grade = models.CharField(max_length=2)
    Points = models.IntegerField()
    
    
    class Meta:
        db_table = 'BTGradePoints'
        unique_together = (('Regulation', 'Grade', 'Points'))
        managed = True


