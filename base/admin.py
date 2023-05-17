from django.contrib import admin

# Register your models here.
from .models import BTMCourses
from .models import BTMSubjects
from .models import BTMSubjectInfo
from .models import BTMStudentRegistrations
from .models import BTMMarksDistribution
from .models import BTMCourseStructure
from .models import BTMMarks
from .models import BTMStudentGrades
from .models import BTMGradePoints
from .models import BTMGradesThreshold
from .models import BTMStudentGradePoints

admin.site.register(BTMStudentGradePoints)
admin.site.register(BTMGradePoints)
admin.site.register(BTMGradesThreshold)
admin.site.register(BTMMarksDistribution)
admin.site.register(BTMCourseStructure)
admin.site.register(BTMMarks)
admin.site.register(BTMStudentGrades)
admin.site.register(BTMSubjects)
admin.site.register(BTMSubjectInfo)
admin.site.register(BTMStudentRegistrations)
admin.site.register(BTMCourses)