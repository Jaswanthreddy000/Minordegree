from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import BTMStudentRegistrations, BTMCourses, BTMMarksDistribution, BTMStudentGradePoints, BTMMarks
from .forms import RollNumberForm


def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def teacherlogin(request):
    return render(request, 'teacherlogin.html')

def entermarks(request):
    return render(request, 'entermarks.html')

def result(request):
    return render(request, 'result.html')


from .models import BTMMarksDistribution
from .forms import MarksDistributionForm

def marks_distribution(request):
    if request.method == 'POST':
        form = MarksDistributionForm(request.POST)
        if form.is_valid():
            marks_distribution = BTMMarksDistribution.objects.create(
                Regulation=form.cleaned_data['Regulation'],
                Distribution=form.cleaned_data['Distribution'],
                DistributionNames=form.cleaned_data['DistributionNames'],
                PromoteThreshold=form.cleaned_data['PromoteThreshold'],
            )
            marks_distribution.save()
            return render(request, 'success.html')
    else:
        form = MarksDistributionForm()
    return render(request, 'marks_distribution.html', {'form': form})


def calculate_sgpa(request):
    if request.method == 'POST':
        form = RollNumberForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            student_registrations = BTMStudentRegistrations.objects.filter(student__roll_no=roll_number).select_related('sub_id__course')
            total_credit_points = 0
            total_credits = 0
       
            for registration in student_registrations:
                course = registration.sub_id.course
                credits = course.Credits
                marks = BTMMarks.objects.filter(Registration=registration).first()
                distribution_ratio = BTMMarksDistribution.objects.filter(course=course, Regulation=registration.RegEventId.Regulation).first().DistributionRatio.split(':')
                total_marks = marks.get_total_marks()
                for ratio in distribution_ratio:
                    if total_marks >= float(ratio):
                        grade = BTMMarksDistribution.objects.filter(course=course, Regulation=registration.RegEventId.Regulation, Ratio=ratio).first().Grade
                        break
                grade_points = BTMStudentGradePoints.objects.filter(Grade=grade).first().Points
                total_credit_points += (credits * grade_points)
                total_credits += credits
                sgpa = total_credit_points / total_credits
                return HttpResponseRedirect(reverse('sgpa', args=[roll_number, sgpa]))
    else:
        form = RollNumberForm()
    return render(request, 'roll_number.html', {'form': form})
       