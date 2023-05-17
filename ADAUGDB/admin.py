from django.contrib import admin

# Register your models here.
from .models import BTRegistrationStatus
from .models import BTCourseStructure
from .models import BTCourses
from .models import BTMarksDistribution
from .models import BTGradePoints



admin.site.register(BTGradePoints)
admin.site.register(BTRegistrationStatus)
admin.site.register(BTCourseStructure)
admin.site.register(BTCourses)
admin.site.register(BTMarksDistribution)

