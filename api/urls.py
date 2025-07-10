from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('patients/', views.patient_list, name='patient_list'),
    path('add_patient/', views.add_patient, name='add_patient'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),

    path('mappings/', views.manage_mappings, name='manage_mappings'),
    path('', views.home_redirect, name='home'),

    path('patients/<int:id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:id>/edit/', views.update_patient, name='update_patient'),
    path('patients/<int:id>/delete/', views.delete_patient, name='delete_patient'),

    path('doctors/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:id>/edit/', views.update_doctor, name='update_doctor'),
    path('doctors/<int:id>/delete/', views.delete_doctor, name='delete_doctor'),

    path('patients/<int:patient_id>/doctors/', views.view_patient_doctors, name='view_patient_doctors'),
    path('mappings/<int:id>/remove/', views.remove_mapping, name='remove_mapping'),

]
