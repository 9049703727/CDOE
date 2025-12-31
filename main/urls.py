from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact.html', views.contact, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('courses.html', views.courses_list, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:slug>/enroll/', views.course_enroll, name='course_enroll'),
    path('<path:filename>.html', views.serve_html, name='serve_html'),
    
]



