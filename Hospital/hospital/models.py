from django.db import models
from django.core.validators import RegexValidator
SEX_OPTIONS = (
        ('SEX_FEMALE', 'Female'),
        ('SEX_MALE', 'Male'),
        ('SEX_UNSURE', 'Unsure')
    )
# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=45)
    message=models.CharField(max_length=250)

class Subscribe(models.Model):
    email=models.CharField(max_length=45)

class Doctor(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True,validators=[
        RegexValidator(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            message='Enter a valid email')])
    password=models.CharField(max_length=30,validators=[
        RegexValidator(r'[A-Za-z0-9@#$%^&+=]{8,}',
            message='password must be Alphanumeric(Ex:-Aasd@12s)')])
    phone=models.CharField(max_length=30,validators=[
        RegexValidator(r'[6789][0-9]{9,}',
            message='Enter a valid phone number')])
    gender=models.CharField(max_length=10)
    location=models.CharField(max_length=255)

class Admin(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=10)
    location=models.CharField(max_length=255)


class Patient(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True,validators=[
        RegexValidator(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            message='Enter a valid email')])
    password=models.CharField(max_length=30,validators=[
        RegexValidator(r'[A-Za-z0-9@#$%^&+=]{8,}',
            message='password must be Alphanumeric(Ex:-Aasd@12s)')])
    phone=models.CharField(max_length=30,validators=[
        RegexValidator(r'[6789][0-9]{9,}',
            message='Enter a valid phone number')])
    gender=models.CharField(max_length=10)
    location=models.CharField(max_length=255)

class Pharmacy(models.Model):
    pharmacy=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    phone=models.BigIntegerField()

class Appointment(models.Model):
    patient_id=models.CharField(max_length=20,default=None)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=10)
    location=models.CharField(max_length=255)
    speciality=models.CharField(max_length=30)
    doctors=models.CharField(max_length=30)
    date=models.CharField(max_length=30)
    time=models.CharField(max_length=30)
    symptoms=models.CharField(max_length=30)
    problems=models.CharField(max_length=30)
    report_boolean = models.BooleanField(default=False)
    report = models.FileField(upload_to='media/', default=None)
    prescription_boolean = models.BooleanField(default=False)
    prescription = models.FileField(upload_to='media/', default=None)
    age=models.IntegerField()
    Lab_report=models.BooleanField(default=False)
    doctor = models.CharField(max_length=30, default="")
    doctor_email = models.CharField(max_length=30, default="")


class Lab(models.Model):
    pharmacy=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=10)
    location=models.CharField(max_length=255)

class Pharmacyord(models.Model):
    pharmacy_name=models.CharField(max_length=30)
    patient_id=models.CharField(max_length=30)
    file=models.FileField(upload_to='media/')
    patient_name=models.CharField(max_length=30)
    patient_email=models.CharField(max_length=30)
    patient_phone=models.CharField(max_length=30)
    doctor=models.CharField(max_length=30)
    doctor_email=models.CharField(max_length=30)
    delivery=models.BooleanField(default=False)
    order_status=models.BooleanField(default=False)
    amount=models.IntegerField(default=0)
    payment=models.CharField(default="", max_length=30)


class Tablet(models.Model):
    image=models.FileField(upload_to='media/')
    name=models.CharField(max_length=30)
    dosages=models.CharField(max_length=30)
    problems=models.CharField(max_length=30)
    price=models.IntegerField()
    stock=models.IntegerField()
    pharmacy=models.CharField(max_length=30)
    severity=models.CharField(max_length=20,default='high')

class reqPharmacy(models.Model):
    pharmacy=models.CharField(max_length=30)
    tablet=models.CharField(max_length=30)
    dosage=models.CharField(max_length=30)
    pharmacy_boolean=models.BooleanField(default=False)
    accepted_pharmacy=models.CharField(max_length=30,default="")
    recomended=models.CharField(max_length=30,default="")
    doctor=models.CharField(default="",max_length=30)
    doctor_booln=models.BooleanField(default=False)
    doctor_boolean=models.BooleanField(default=False)
    patient_id=models.CharField(default="",max_length=30)

class Lab_records(models.Model):
    patient_id=models.CharField(max_length=30)
    problems=models.CharField(max_length=30)
    report_details=models.CharField(max_length=30)
    file=models.FileField(upload_to='media/')
