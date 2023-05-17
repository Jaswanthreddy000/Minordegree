from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
     path('teacherlogin/',views.teacherlogin,name="teacherlogin"),
    path('entermarks/',views.entermarks,name="entermarks"),
     path('result/',views.result,name="result"),
    path('marks_distribution/', views.marks_distribution, name='marks_distribution'),
    path('sgpa/',views.calculate_sgpa,name="sgpa"), 
     


]
