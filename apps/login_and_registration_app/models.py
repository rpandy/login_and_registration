# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

LETTERS_ONLY = re.compile(r'[A-Za-z]')

# Create your models here.
class UserManager(models.Manager):
    #handles validations & database queries
    def validate_and_create(self,data):
        print data, "<<--here is the data from the validations and/or database"

        replicated = User.objects.filter(email=data['email'])

        errors = []
        #validate first name (2+ char/ Letters only/ cannot be empty)
        if len(data['first_name']) < 2:
            print "First name must be at least 2 characters"
            errors.append("First name must be at least 2 characters")
        if not LETTERS_ONLY.match(data['first_name']):
            print "First name must contain letters only"
            errors.append("First name must contain letters only")
        #validate last name (2+ char/ Letters only/ cannot be empty)
        if len(data['last_name']) < 2:
            print "Last name must be at least 2 characters"
            errors.append("Last name must be at least 2 characters")
        if not LETTERS_ONLY.match(data['last_name']):
            print "Last name must contain letters only"
            errors.append("Last name must contain letters only")
        #validate email (valid email format/ cannot be empty/ email must be original)
        if len(data['email']) < 1:
            print "Email cannot be blank"
            errors.append("Email cannot be blank")
        if not EMAIL_REGEX.match(data['email']):
            print "Email is not valid"
            errors.append("Email is not valid")
        if len(replicated) > 0:
            print "Email has already been registered"
            errors.append("Email has already been registered")
        #validate password (at least 8 characters/ cannot be empty)
        if len(data['password']) < 8:
            print "Password must be at least 8 characters long"
            errors.append("Password must be at least 8 characters long")
        #validate password confirmation(match password)
        if data['password'] != data['password_confirmation']:
            print "Passwords do not match"
            errors.append("Passwords do not match")
        # if email_entered == replicated.email:

        if errors:
            return (False, errors)
        else:
            #Bcrypt encryption
            pw = data['password']
            hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

            new_object = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = hashed_pw, #<---HASHED PASSWORD
            )
            return (True, new_object)
    def validate_and_login(self,data):
        #validate email (valid email format/ cannot be empty)
        # Review the use of filter here vs GET
        User_Exists = User.objects.filter(email=data['email'])
        print User_Exists, "<--- replicated"
        errors = []
        if len(data['email']) < 1:
            print "Email and password combination does not exist"
            errors.append("Email and password combination does not exist")
        if not EMAIL_REGEX.match(data['email']):
            print "Email is not valid"
            errors.append("Email is not valid")
        #Check to see if email address entered is in database
        if len(User_Exists) == 0:
            print "Email is not registered"
            errors.append("Email is not registered")
        #validate password (at least 8 characters/ cannot be empty)
        if len(data['password']) < 8:
            print "Password must be at least 8 characters long"
            errors.append("Password must be at least 8 characters long")
        if errors:
            return (False, errors)
        else:
            #used get because we're only looking for one particular email address. Can we use same variable from before. TEST
            login_user = User.objects.get(email=data['email'])
            # login_user = User_Exists
            pw = data['password']

            # hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            if bcrypt.hashpw(pw.encode(), login_user.password.encode()) == login_user.password.encode():
            # if bcrypt.checkpw(pw.encode(), login_user.password.encode()):
                print "the passwords match"
                return (True, login_user)
            else:
                print "the passwords DONT match"
                errors.append("Invalid Password")
                return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length = 75)
    last_name = models.CharField(max_length = 75)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    created_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)

    objects = UserManager()
