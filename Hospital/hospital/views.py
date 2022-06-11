import json
import os.path
import random
import string
import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect, Http404
from .models import Subscribe, Contact, Pharmacy, Patient, Doctor, Appointment, Tablet, Lab, Admin, Pharmacyord, \
    reqPharmacy, Lab_records
from django.contrib import messages
from django.db import IntegrityError
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from datetime import date, datetime, time
from .forms import *
from django.views.generic import *
import numpy as np

global a
a = {}


# Create your views here.
def home(request):
    if request.method == 'POST':
        global a

        a = {'speciality': request.POST.get('speciality'), 'doctors': request.POST.get('doctors'),
             'date': request.POST.get('date'),
             'time': request.POST.get('time'), 'name': request.POST.get('name'), 'number': request.POST.get('number'),
             'email': request.POST.get('email'), 'problems': request.POST.get('problems')}
        return redirect('/patient_login')
    return render(request, 'index-2.html')


def appointment(request):
    return HttpResponse(request.POST.get('type'))


def about(request):
    return render(request, 'about-us.html')


def services(request):
    return render(request, 'services.html')


def news(request):
    return render(request, 'blog.html')


def contact(request):
    return render(request, 'contact.html')


def patient_login(request):
    if 'patient_name' in request.session:
        return redirect('/patient_page')
    else:
        if request.method == "POST":
            try:
                pat = Patient.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
                if pat:
                    patient = Patient.objects.get(email=request.POST.get('email'))
                    request.session['patient_name'] = patient.name
                    request.session['patient_email'] = patient.email
                    return redirect('/appointment_book/')
            except Patient.DoesNotExist:
                messages.error(request, 'check email and password')
                return redirect('/patient_login')
        return render(request, 'login.html', {'name': 'patient'})


class patient_register(FormView):
    template_name = 'register.html'
    form_class = PatientRegisterForm
    success_url = '/patient_login/'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)
        # return render(request, 'register.html',{'name':'doctor','form':})

    def get_context_data(self, **kwargs):
        print(DoctorRegisterForm.as_p)
        context = super().get_context_data(**kwargs)
        context['name'] = 'patient'
        return context

def doctor_login(request):
    if 'doctor_name' in request.session:
        return redirect('/doctor_page/')
    else:
        try:
            if request.method == "POST":
                doctor = Doctor.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
                if doctor:
                    request.session['doctor_name'] = doctor.name
                    request.session['doctor_email'] = doctor.email
                    return redirect('/doctor_page')
        except Doctor.DoesNotExist:
            messages.error(request, 'check email and password')
            return redirect('/doctor_login')
        return render(request, 'login.html', {'name': 'doctor'})


class doctor_register(FormView):
    template_name = 'register.html'
    form_class = DoctorRegisterForm
    success_url = '/doctor_login/'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)
        # return render(request, 'register.html',{'name':'doctor','form':})

    def get_context_data(self, **kwargs):
        print(DoctorRegisterForm.as_p)
        context = super().get_context_data(**kwargs)
        context['name'] = 'doctor'
        return context


def patient_page(request):
    if 'patient_name' in request.session:
        try:
            global a
            id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if request.method == 'POST':
                apo = Appointment()
                apo.patient_id = id
                apo.name = a['name']
                apo.symptoms = request.POST.get('symptoms')
                k = request.POST.get('yes')
                apo.location = request.POST.get('location')
                apo.gender = request.POST.get('gender')
                apo.phone = a['number']
                apo.email = a['email']
                apo.age = request.POST.get('age')
                apo.date = a['date']
                apo.doctors = a['doctors']
                apo.time = a['time']
                apo.problems = a['problems']
                apo.speciality = a['speciality']
                apo.save()
                a = {}
                if k == 'yes':
                    file = request.FILES['file']
                    extensions = os.path.splitext(file.name)[1]
                    name = id + extensions
                    fss = FileSystemStorage()
                    fss.save(name, file)
                    apo.report = name
                messages.success(request, 'successfully uploaded')
                return redirect('/patient_page')
        except KeyError:
            messages.success(request, 'fill the appointment form below')
            return redirect('/appointment_book')
        return render(request, 'patient_page.html')
    else:
        messages.error(request, 'login again')
        return redirect('/patient_login/')


def doctor_page(request):
    if 'doctor_name' in request.session:
        apo = Appointment.objects.filter(doctors=request.session['doctor_name'].capitalize())
        if request.method == 'POST':
            id = request.POST.get('patient_id')
            apo1 = Appointment.objects.get(patient_id=id)
            file = request.FILES['file']
            extensions = os.path.splitext(file.name)[1]
            name = id + 'prescription' + extensions
            fss = FileSystemStorage()
            fss.save(name, file)
            apo1.doctor = request.session['doctor_name']
            apo1.doctor_email = request.session['doctor_email']
            apo1.prescription = name
            apo1.prescription_boolean = True
            apo1.save()
            messages.success(request, 'uploaded')
        return render(request, 'doctor_page.html', {'data': apo})
    else:
        return redirect('/doctor_page')


def doctor_tabreq(request):
    if 'doctor_name' in request.session:
        req = reqPharmacy.objects.filter(doctor=request.session['doctor_name'])
        return render(request, 'doctor_tabreq.html', {'data': req, 'a': a})
    else:
        return redirect('/patient_page')


def doctor_tablet(request, id):
    if 'doctor_name' in request.session:
        req = reqPharmacy.objects.get(pk=id)
        tablet = req.tablet
        dosage = req.dosage
        patient_id = req.patient_id
        tab = Tablet.objects.get(name=tablet, dosages=dosage)
        data = predi(dosage, tab.problems, tab.severity)
        if request.method == 'POST':
            req.recomended = request.POST.get('tablet')
            req.doctor_boolean = True
            req.save()
            apo = Appointment.objects.get(patient_id=patient_id)
            subject = 'tablet changed'
            message = f"Hi {apo.name}, the tablet {tablet} is changed. The new tablet is {request.POST.get('tablet')}"
            from_email = settings.EMAIL_HOST_USER
            recipient_mail = [apo.email]
            send_mail(subject, message, from_email, recipient_mail)
            messages.success(request, 'updated successfully')
            return redirect('/doctor/tablet_request')
        return render(request, 'doctor_tabreq1.html', {'d': req, 'data': data})
    else:
        return redirect('/patient_page')


def predi(dosage, problem, severity):
    a = []
    yt = []
    filename = f"{settings.MEDIA_ROOT}/dataset.csv"
    dataset = pd.read_csv(filename)
    prob = {'pain': 1, 'fever': 2, 'cold': 3, 'diabetes': 4, 'headache': 5}
    seve = {'low': 1, 'high': 3, 'medium': 2}
    xt = [[dosage, prob[problem], seve[severity]]]
    for i in range(1, 10):
        x = dataset.iloc[:, 2:]
        y = dataset.iloc[:, 1:2]
        labelencoder = LabelEncoder()
        ytrain = labelencoder.fit_transform(y)
        std = StandardScaler()
        xtrain = std.fit_transform(x)

        classifier = RandomForestClassifier()
        classifier.fit(x, ytrain)

        ypred = classifier.predict(xt)
        ypredicted = labelencoder.inverse_transform(ypred)
        print(ypredicted)
        a.append(ypredicted)

    for i in a:
        if i not in yt:
            yt.append(i[0])

    return yt


def doctor_logout(request):
    request.session.pop('doctor_name', None)
    request.session.pop('doctor_email', None)
    messages.success(request, 'successfully logged out')
    return redirect('/')


def patient_logout(request):
    request.session.pop('patient_name', None)
    request.session.pop('patient_email', None)
    messages.success(request, 'successfully logged out')
    return redirect('/')


def appointmen(request):
    if 'patient_name' in request.session:
        apo = Appointment.objects.filter(email=request.session['patient_email'])
        return render(request, 'appointment.html', {'data': apo})

    else:
        return redirect('/patient_login/')


def appointment_book(request):
    if 'patient_name' in request.session:
        if request.method == 'POST':
            global a
            a = {'speciality': request.POST.get('speciality'), 'doctors': request.POST.get('doctors'),
                 'date': request.POST.get('date'),
                 'time': request.POST.get('time'), 'name': request.POST.get('name'),
                 'number': request.POST.get('number'),
                 'email': request.POST.get('email'), 'problems': request.POST.get('problems')}
            return redirect('/patient_login')
        return render(request, 'appointment_book.html')
    else:
        return redirect('/patient_login/')


def pharmacy_book(request):
    if 'patient_name' in request.session:
        if request.method == "POST":
            id = request.POST.get('patient_id')
            apo = Appointment.objects.get(patient_id=id)
            pharmacy = Pharmacyord()
            pharmacy.patient_name = apo.name
            pharmacy.patient_email = apo.email
            pharmacy.patient_phone = apo.phone
            file = request.FILES['file']
            extensions = os.path.splitext(file.name)[1]
            name = id + 'pharmacy' + extensions
            fss = FileSystemStorage()
            fss.save(name, file)
            pharmacy.pharmacy_name = request.POST.get('pharmacy')
            pharmacy.patient_id = id
            pharmacy.doctor = apo.doctor
            pharmacy.doctor_email = apo.doctor_email
            pharmacy.file = name
            pharmacy.save()
            messages.success(request, 'pharmacy report sent successfully')
            return redirect(f'/pharmacy_book')
        return render(request, 'pharmacy_book.html')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def lab_login(request):
    email = 'lab'
    password = '1234'
    if 'lab_email' in request.session:
        return redirect('/lab_page/')
    else:
        if request.method == "POST":
            if email == request.POST.get('email'):
                if password == request.POST.get('password'):
                    request.session['lab_email'] = email
                    return redirect('/lab_page')
                else:
                    messages.success(request, 'password is wrong')
                    return redirect('/lab_login')
            else:
                messages.success(request, 'email id is wrong')
                return redirect('/lab_login')
        return render(request, 'lab_login.html', {'name': 'lab'})


def lab_page(request):
    if 'lab_email' in request.session:
        apo = Appointment.objects.filter(Lab_report=True, report_boolean=False)
        if request.method == "POST":
            id = request.POST.get('patient_id')
            apo1 = Appointment.objects.get(patient_id=id)
            file = request.FILES['file']
            extensions = os.path.splitext(file.name)[1]
            name = id + extensions
            fss = FileSystemStorage()
            fss.save(name, file)
            apo1.report = name
            apo1.report_boolean = True
            apo1.save()
        return render(request, 'lab_page.html', {'data': apo})
    else:
        messages.error(request, 'login again')
        return redirect('/lab_login')


def lab_request(request, id):
    if 'patient_name' in request.session:
        try:
            apo = Appointment.objects.get(patient_id=id)
            apo.Lab_report = True
            apo.save()
            messages.success(request, 'request sent successfully')
            return redirect('/appointment')
        except KeyError:
            messages.success(request, 'fill the appointment form below')
            return redirect('/appointment_book')


def lab_works(request):
    if 'lab_email' in request.session:
        apo = Appointment.objects.filter(Lab_report=True)
        return render(request, 'lab_page.html', {'data': apo})
    else:
        messages.error(request, 'login again')
        return redirect('/')


def lab_records(request):
    if 'lab_email' in request.session:
        lab = Lab_records.objects.all()
        return render(request, 'lab_records.html', {'data': lab})
    else:
        messages.error(request, 'login again')


def lab_records_upload(request):
    if 'lab_email' in request.session:
        if request.method == 'POST':
            lab = Lab_records()
            lab.patient_id = request.POST.get('patient_id').upper()
            lab.problems = request.POST.get('problems')
            file = request.FILES['file']
            extensions = os.path.splitext(file.name)[1]
            name = request.POST.get('patient_id') + extensions
            fss = FileSystemStorage()
            fss.save(name, file)
            lab.file = name
            lab.report_details = request.POST.get('report')
            lab.save()
            messages.success(request, 'Uploaded Successfully')
            return redirect('/record_upload')
        return render(request, 'lab-upload.html')
    else:
        messages.error(request, 'login again')


def lab_logout(request):
    request.session.pop('lab_email', None)
    messages.success(request, 'successfully logged out')
    return redirect('/')


def admin_login(request):
    if 'admin_name' in request.session:
        return redirect('/admin_page/')
    else:
        try:
            if request.method == "POST":
                email = request.POST.get('email')
                password = request.POST.get('password')
                if email == 'admin@gmail.com' and password == 'admin':
                    request.session['admin_name'] = 'admin'
                    request.session['admin_email'] = 'admin@gmail.com'
                    return redirect('/admin_page')
        except Admin.DoesNotExist:
            messages.error(request, 'check email and password')
            return redirect('/admin_login')
        return render(request, 'login.html', {'name': 'admin'})


def admin_page(request):
    if 'admin_name' in request.session:
        apo = Patient.objects.all()
        return render(request, 'admin_page.html', {'data': apo, 'a': 'Patient'})
    else:
        messages.error(request, 'login again')
        return redirect('/admin_login')


def admin_logout(request):
    request.session.pop('admin_name', None)
    request.session.pop('admin_email', None)
    messages.success(request, 'successfully logged out')
    return redirect('/')


def appointment_list(request):
    if 'admin_name' in request.session:
        apo = Appointment.objects.all()
        return render(request, 'Appointment_list.html', {'data': apo, 'a': 'doctor'})
    else:
        messages.error(request, 'login again')
        return redirect('/admin_login')


def doctor_list(request):
    if 'admin_name' in request.session:
        apo = Doctor.objects.all()
        return render(request, 'admin_page.html', {'data': apo, 'a': 'doctor'})
    else:
        messages.error(request, 'login again')
        return redirect('/admin_login')


def lab_list(request):
    if 'admin_name' in request.session:
        apo = Doctor.objects.all()
        return render(request, 'admin_page.html', {'data': apo, 'a': 'doctor'})
    else:
        messages.error(request, 'login again')
        return redirect('/admin_login')


def pharmacy_login(request, name):
    if 'pharmacy_email' in request.session:
        return redirect(f'/pharmacy_page/{name}')
    else:
        try:
            if request.method == "POST":
                pharmacy = Pharmacy.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
                if pharmacy:
                    request.session['pharmacy_email'] = pharmacy.email
                    request.session['pharmacy_pharmacy'] = pharmacy.pharmacy
                    return redirect(f'/pharmacy_page/{name}')
        except Doctor.DoesNotExist:
            messages.error(request, 'check email and password')
            return redirect(f'/pharmacy_login/{name}')
        return render(request, 'pharmacy_login.html', {'name': name})


def pharmacy_page(request, name):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        tablet = Tablet.objects.filter(pharmacy=name)
        return render(request, 'pharmacy_page.html', {'name': name, 'data': tablet})
    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def tablet(request):
    name = 'kumar'
    if request.method == 'POST':
        tab = Tablet()
        tablet = request.POST.get('name')
        dosages = request.POST.get('tablet_mg')
        tab.pharmacy = name
        image = request.FILES['image']
        extensions = os.path.splitext(image.name)[1]
        name = tablet + dosages + extensions
        fss = FileSystemStorage()
        fss.save(name, image)
        tab.image = name
        tab.name = request.POST.get('name')
        tab.problems = request.POST.get('problems')
        tab.dosages = request.POST.get('tablet_mg')
        tab.price = request.POST.get('price')
        tab.stock = request.POST.get('stock')
        tab.severity = request.POST.get('severity')
        tab.save()
    return render(request, 'tablet.html', {'name': name})


def pharmacy_orders(request, name):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        order = Pharmacyord.objects.filter(pharmacy_name=name)
        if request.method == "POST":
            req = reqPharmacy()
            req.pharmacy = name
            req.tablet = request.POST.get('tablet')
            req.dosage = request.POST.get('dosage')
            req.patient_id = request.POST.get('patient_id')
            req.save()
            messages.success(request, 'updated successfully')
        return render(request, 'pharmacy_orders.html', {'name': name, 'data': order})

    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def pharmacy_req(request, name):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        req = reqPharmacy.objects.all()
        return render(request, 'pharmacy_req.html', {'data': req, 'name': name})
    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def accept(request, pk, name):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        req = reqPharmacy.objects.get(pk=pk)
        req.accepted_pharmacy = name
        req.pharmacy_boolean = True
        req.save()
        return redirect(f'/pharmacy/{name}/request')
    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def tabReqDoctor(request, name, pk):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        req = reqPharmacy.objects.get(pk=pk)
        p_id = req.patient_id
        apo = Appointment.objects.get(patient_id=p_id)
        req.doctor = apo.doctors
        req.save()
        return redirect(f'/pharmacy/{name}/request')
    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def delivery(request, id, name):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        ord = Pharmacyord.objects.get(patient_id=id)
        ord.delivery = True
        ord.save()
        messages.success(request, 'deliverd successfully')
        return redirect(f'/pharmacy/{name}/orders')
    else:
        messages.error(request, 'login again')
        return redirect(f'/pharmacy_page/{name}')


def pharmacy_logout(request):
    if 'pharmacy_email' in request.session:
        request.session.pop('pharmacy_name', None)
        request.session.pop('pharmacy_pharmacy', None)
        request.session.pop('pharmacy_email', None)
        messages.success(request, 'logout successfully')
        return redirect('/')
    else:
        messages.success(request, 'login again')
        return redirect('/')


def confirm_order(request, name, id):
    if ('pharmacy_email' in request.session) & (request.session['pharmacy_pharmacy'] == name):
        ord = Pharmacyord.objects.get(pk=id)
        if request.method == 'POST':
            ord.order_status = True
            ord.amount = request.POST.get('amount')
            ord.save()
            messages.success(request, 'amount added successfully')
            return redirect(f'/pharmacy/{name}/orders')
        return render(request, 'confirm.html', {'name': name, 'd': ord})
    else:
        messages.success(request, 'login again')
        return redirect('/')


def patient_pharmacy(request):
    if 'patient_name' in request.session:
        ord = Pharmacyord.objects.filter(patient_email=request.session['patient_email'])
        return render(request, 'pahrmacybill.html', {'data': ord})
    else:
        messages.success(request, 'login again')
        return redirect('/patient_login')


def pay(request, id):
    if 'patient_name' in request.session:
        ord = Pharmacyord.objects.get(pk=id)
        if request.method == "POST":
            ord.delivery = True
            ord.payment = request.POST.get('cash')
            ord.save()
            messages.success(request, 'paid successfully')
            return redirect('/Pharmacy_bills')
        return render(request, 'pay.html', {'d': ord})
    else:
        messages.success(request, 'login again')
        return redirect('/patient_login')


def pharmacy_list(request):
    if 'admin_name' in request.session:
        phar = Pharmacy.objects.all()
        return render(request, 'pharmacy_list.html', {'data': phar})
    else:
        messages.success(request, 'login again')
        return redirect('/admin_login')
