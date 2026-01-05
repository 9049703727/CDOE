from django.urls import path
from . import views
from .views import  inquiry_success


urlpatterns = [
    path('', views.index, name='index'),
    path('contact.html', views.contact, name='contact'),
   
    path('courses.html', views.courses_list, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:slug>/enroll/', views.course_enroll, name='course_enroll'),
    path('instructors.html', views.instructors_list, name='instructors_list'),
    path('instructor-profile.html/<int:id>/', views.instructor_detail, name='instructor_detail'),
   
    path('inquiry-success/', inquiry_success, name='inquiry_success'),
    path('iks-course/<slug:slug>/', views.iks_course_registration, name='iks_course_registration'),

    path('technical-staff/', views.technical_staff, name='technical_staff'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('notifications/', views.notifications_view, name='notifications'),
    path('inquiry/', views.inquiry_form, name='inquiry_form'),

    path('contact/', views.contact_page, name='contact_page'),
    path('administration/', views.admin_staff_list, name='admin_staff_list'),
    path('<path:filename>.html', views.serve_html, name='serve_html'),



]



