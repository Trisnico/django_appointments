# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import * 
from datetime import date


# Create your views here.
def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'appointment_app/main.html')

def register(request):
    user = User.objects.validate_registration(request.POST)
    if user[0]:
        for fail in user[0]:
            messages.error(request, fail)
        return redirect('/')
    request.session['id'] = user[1].id
    return redirect('/appointments')

def login(request):
    user = User.objects.validate_login(request.POST)
    if user[0]:
        for fail in user[0]:
            messages.error(request, fail)
        return redirect('/')
    request.session['id'] = user[1].id
    return redirect('/appointments')

def logout(request):
    del request.session['id']
    return redirect('/')

def user_login(request):
    if 'id' not in request.session:
        return redirect('/')

def appointments(request):
    user_login(request)
    all_appointments = Appointment.objects.all()
    sort_date = all_appointments.order_by("-time")
    context = {
        "sort_date": sort_date,
        "user": User.objects.get( id = request.session['id']),
        "time": date.today(), 
        "appointments": Appointment.objects.filter(user_id=request.session['id']).exclude(date=date.today()),
        "today_appointment": Appointment.objects.filter(user_id=request.session['id']).filter(date = date.today())  
    }
    return render(request, 'appointment_app/appointments.html', context)

def add(request):
        add_appointment = Appointment.objects.appointment_validation(request.POST, request.session['id'])
        if add_appointment[0]:
            for errs in add_appointment[0]:
                messages.error(request, errs)
            return redirect('/appointments')
        return redirect("/appointments")

def edit(request, appointment_id):
    user_login(request)
    appointment = Appointment.objects.get(id = appointment_id)
    context = {
        "appointment": appointment
    }
    return render(request, "appointment_app/update.html", context)

def update(request, appointment_id):
    user_login(request)
    update_appointment = Appointment.objects.edit_appointment(request.POST, appointment_id)
    if update_appointment[0]:
        for errs in update_appointment[0]:
            messages.error(request, errs)
        return redirect('/appointments/'+ appointment_id)
    messages.success(request, "Update Successful")
    return redirect('/appointments')

def delete(request, appointment_id):
    user = User.objects.get(id=request.session["id"])
    appointment = Appointment.objects.get(id=appointment_id)
    if appointment.user == user:
        appointment.delete()
    return redirect("/appointments")
  