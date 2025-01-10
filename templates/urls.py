from django.urls import path 
from .import views

urlpatterns = [
    path("",views.HomePage,name="HomePage"),   
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),    
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("user_type_confirmation",views.user_type_confirmation,name="user_type_confirmation"),
    path("student_confirm",views.student_confirm,name="student_confirm"),
    path("teacher_confirm",views.teacher_confirm,name="teacher_confirm"),
    path("teacher_index",views.teacher_index,name="teacher_index"),
    path("student_details",views.student_details,name="student_details"),
    path("teacher_details",views.teacher_details,name="teacher_details"),
    path("add_student",views.add_student,name="add_student"),
    path("add_teacher",views.add_teacher,name="add_teacher"),
    path("update_student/<int:student_id>",views.update_student,name="update_student"),
    path("update_teacher/<int:id>",views.update_teacher,name="update_teacher"),
    path("register_student",views.register_student,name="register_student"),
    path("delete_student/<int:id>",views.delete_student,name="delete_student"),
    # path("delete_teacher/<int:id>",views.delete_teacher,name="delete_teacher"),
    path("verified_users/<int:pk>",views.verified_users,name="verified_users"),
 
   
    ]
