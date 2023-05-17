from django.contrib import admin

# Register your models here.
from .models import BTMarks
from .models import BTStudentGrades



admin.site.register(BTMarks)
admin.site.register(BTStudentGrades)
