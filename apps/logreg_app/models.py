from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "This email address already has an account"
        if len(postData['password']) < 8:
            errors['password'] = "Password needs to be at least 8 characters"
        elif postData['password'] != postData['conf_password']:
            errors['password'] = "Passwords do not mach"
        return errors
    
    def validate_login(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email address is not valid"
        elif not user:
            errors['email'] = "This email does not exist"
        else:
            if len(postData['password']) < 8:
                errors['email'] = "Password needs to be at least 8 characters"
            elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                print("Passwords Match")
            else:
                errors['password'] = "This is not a valid password"
        return errors

class User(models.Model):
    first_name = models.CharField(default="first name*", max_length=60)
    last_name = models.CharField(default="first name*", max_length=60)
    email = models.CharField(default="first name*", max_length=60)
    password = models.CharField(default="password*", max_length=90)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User ID: ({self.id})| First Name: {self.first_name}| Last Name: {self.last_name}| Email: {self.email}| Password: {self.password} ||"