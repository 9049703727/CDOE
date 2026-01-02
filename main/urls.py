from django.urls import path
from . import views
from .views import inquiry_form, inquiry_success


urlpatterns = [
    path('', views.index, name='index'),
    path('contact.html', views.contact, name='contact'),
   
    path('courses.html', views.courses_list, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:slug>/enroll/', views.course_enroll, name='course_enroll'),
    
    path('inquiry/', inquiry_form, name='inquiry'),
    path('inquiry-success/', inquiry_success, name='inquiry_success'),
    path('iks-course/<slug:slug>/', views.iks_course_registration, name='iks_course_registration'),
  
    path('notifications/', views.notifications_view, name='notifications'),
    path('technical-staff/', views.technical_staff, name='technical_staff'),
    path('<path:filename>.html', views.serve_html, name='serve_html'),

]



