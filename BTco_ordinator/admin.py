from django.contrib import admin

# Register your models here.
from .models import BTRollLists
from .models import BTStudentGradePoints
from .models import BTSubjects
from .models import BTSubjectInfo
from .models import BTStudentRegistrations



admin.site.register(BTStudentGradePoints)
admin.site.register(BTSubjects)
admin.site.register(BTSubjectInfo)
admin.site.register(BTStudentRegistrations)
admin.site.register(BTRollLists)