from __future__ import unicode_literals
import bcrypt
from django.db import models
from datetime import datetime


# Create your models here.
class UserManager(models.Manager):
    def validate(self, post_data):
        # the_user = []
        errors = [] # populate list of strings that returns back to views.py
        # first_name 2 or more
        if len(post_data['name']) < 3:
            errors.append("Name must be more than 3 characters")
        # last_name 2 or more
        if len(post_data['username']) < 3:
            errors.append("Last name must be more than 3 characters")
        if self.filter(username=post_data['username']):
            errors.append("Username exists already")
        # password 8 or more
        if len(post_data['password']) < 8:
            errors.append("Password must be more than 8 characters")
        # confirm password
        if post_data['password'] != post_data['confirm_password']:
            errors.append("Confirm password must match Password")
        return errors #funtion will return a list


    def create_user(self, clean_data):
        hashed = bcrypt.hashpw(clean_data['password'].encode(), bcrypt.gensalt())
        return self.create(
            name = clean_data['name'],
            username = clean_data['username'],
            password = hashed
        )

    def validate_login(self, post_data):
        """
        check post request for valid data
        if valid, returns tuple ([], <User Object>)
        if not, returns ([error list], None)
        """
        errors = []
        the_user = None
        #email is not in system
        if not self.filter(username=post_data['username']):
            errors.append("Incorrect username/password")
        else:
            the_user = self.get(username=post_data['username'])
            #password is incorrect
            if not bcrypt.checkpw(post_data['password'].encode(), the_user.password.encode()):
                errors.append("Incorrect username/password")
                the_user = None
        return (errors, the_user)


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return self.name

class TripManager(models.Manager):
    def validate_trip(self, post_data):
        errors = []
        if len(post_data['start_date']) < 1 and len(post_data['end_date']) < 1:
                errors.append("dates must not be blank")
        else:
            startdate = datetime.strptime(post_data['start_date'], "%Y-%m-%d")
            enddate = datetime.strptime(post_data['end_date'], "%Y-%m-%d")
            if startdate < datetime.today():
                errors.append("Start date must be future dated")
            if enddate < startdate:
                errors.append("End date must be after start date")
        if len(post_data['destination']) < 1 and len(post_data['plan']) < 1:
            errors.append("Fields must not be empty")
        return errors

    def create_trip(self, post_data, user_id):
        return self.create(
            destination = post_data['destination'],
            start_date = post_data['start_date'],
            end_date = post_data['end_date'],
            plan = post_data['plan'],
            creator = User.objects.get(id=user_id)
        )
class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='trips')
    followers = models.ManyToManyField(User, related_name='follows')

    objects = TripManager()
    def __str__(self):
        return self.destination
