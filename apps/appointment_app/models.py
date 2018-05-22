# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date, datetime
from django.utils import timezone
import re
import bcrypt


# Create your models here.

class userManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        user = None
        for key, value in postData.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break
        if len(postData['name']) < 3:
            errors.append("Name must be 3 letters or more")
        if not re.search(r'\w+\@\w+.\w+', postData['email']):
			errors.append('Must enter a valid email')
        if postData['password'] != postData['password_confirm']:
            errors.append("Your passwords don't match")
        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")
        if postData['birthday'] == '':
            errors.append("Enter Date of Birth")
        if not errors:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(
                name = postData['name'],
                email = postData['email'],
                birthday = postData['birthday'],
                password = hashed_pw
            )
        return errors, user

    def validate_login(self, postData):
        errors = []
        user = None
        if not self.filter(email = postData['email']):
            errors.append("Invalid user/password")
        else:
            user = self.get(email = postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append("Invalid user/password")
        return errors, user

class User(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class appointmentManager(models.Manager):
    def appointment_validation(self, postData, id):
        errors = []
        add_appointment = None
        print postData['time']
        print datetime.now().strftime("%H:%M")
        for key, value in postData.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break
        if not postData['date'] >= unicode(date.today()):
            errors.append("Date must be today or in the Future")
        if len(postData["date"]) == "":
            errors.append("Must enter Date")
        if len(postData['tasks']) == 0:
            errors.append("Task cannnot be blank")
        if not errors:
            add_appointment = self.create(
                user = User.objects.get(id = id),
                tasks = postData['tasks'],
                date = postData['date'],
                time = postData['time'],
                status = "Pending"
            )
        return errors, add_appointment

    def edit_appointment(self, postData, app_id):
        errors = []
        update_appointment = None
        for key, value in postData.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break
        if not postData['edit_date'] >= unicode(date.today()):
            errors.append("Date must be today or in the Future")
        if len(postData["edit_date"]) == "":
            errors.append("Must enter Date")
        if len(postData['edit_tasks']) == 0:
            errors.append("Task cannnot be blank")
        if not errors:
            update_appointment = self.filter(id = app_id).update(
                tasks = postData['edit_tasks'],
                status = postData['edit_status'],
                date = postData['edit_date'],
                time = postData['edit_time']
            )        
        return errors, update_appointment

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name = "user")
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    tasks = models.TextField(max_length=255)
    status = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = appointmentManager()