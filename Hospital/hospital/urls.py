"""HospitalManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_register/', views.patient_register.as_view(), name='patient_register'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_register/', views.doctor_register.as_view(), name='doctor_register'),
    path('doctor_page/', views.doctor_page, name='doctor_page'),
    path('patient_page/', views.patient_page, name='patient_page'),
    path('pharmacy_page/<str:name>', views.pharmacy_page, name='pharmacy_page'),
    path('appointment/', views.appointmen, name='appointment'),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
    path('patient_logout/', views.patient_logout, name='patient_logout'),
    path('download/<str:path>', views.download, name='download'),
    path('request/<str:id>', views.lab_request, name='lab_request'),
    path('lab_login/', views.lab_login, name='lab_login'),
    path('lab_page/', views.lab_page, name='lab_page'),
    path('appointment_book/', views.appointment_book, name='appointment_book'),
    path('lab_works/', views.lab_works, name='lab_works'),
    path('lab_logout/', views.lab_logout, name='lab_logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    #path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('lab_list/', views.lab_list, name='lab_list'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('pharmacy_book/', views.pharmacy_book, name='pharmacy_book'),
    path('pharmacy_login/<str:name>', views.pharmacy_login, name='pharmacy_login'),
    path('pharmacy/tablet', views.tablet, name='pharmacy_tablet'),
    path('pharmacy/<str:name>/orders', views.pharmacy_orders, name='pharmacy_orders'),
    path('pharmacy/<str:name>/request', views.pharmacy_req, name='pharmacy_req'),
    path('accept/<str:name>/<int:pk>', views.accept, name='accept'),
    path('<str:name>/doctor/<int:pk>', views.tabReqDoctor, name='tabReqDoctor'),
    path('doctor/tablet_request', views.doctor_tabreq, name='doctor_tabreq'),
    path('doctor/tablet_request/<int:id>', views.doctor_tablet, name='doctor_tablet'),
    path('pharmacy_logout/', views.pharmacy_logout, name='pharmacy_logout'),
    path('<str:name>/delivery/<str:id>', views.delivery, name='delivery'),
    path('record_upload/', views.lab_records_upload, name='record_upload'),
    path('lab_records/', views.lab_records, name='lab_records'),
    path('confirm_order/<str:name>/<int:id>', views.confirm_order, name='confirm_order'),
    path('Pharmacy_bills/', views.patient_pharmacy, name='patient_pharmacy'),
    path('pay/<int:id>', views.pay, name='pay'),
    path('pharmacy_list/', views.pharmacy_list, name='pharmacy_list'),
]