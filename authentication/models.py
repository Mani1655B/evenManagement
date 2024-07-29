from django.contrib.auth.models import User
from django.db import models


# User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('student', 'Student'), ('faculty', 'Faculty'), ('organizer','Oraganizer')], default='student')
    
    def __str__(self):
        return self.user.username

# Event model
class Photos(models.Model):
    photo=models.ImageField( upload_to='images', height_field=None, width_field=None, max_length=None)
    event=models.ForeignKey("Event", on_delete=models.CASCADE,related_name='images')

    
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=200)
    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

# Task model
class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Registration model
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.event.name}"

# Volunteer model
class Volunteer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteers')
    role = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.user.user.username} - {self.role} - {self.event.name}"

# Resource model
class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ResourceAllocation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='resource_allocations')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocations')
    allocated_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.allocated_quantity} x {self.resource.name} for {self.event.name}"

# Notification model
class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.user.username}"

# Feedback model
class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.user.username} for {self.event.name}"

# Dashboard model
class Dashboard(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='dashboard')
    data = models.JSONField(default=dict)  # Store dashboard data in JSON format

    def __str__(self):
        return f"Dashboard for {self.user.user.username}"
    
class Contact(models.Model):
        name=models.CharField(max_length=50)
        mail=models.EmailField(max_length=254)
        number=models.CharField(max_length=10)
        subject=models.CharField(max_length=50)
        message=models.TextField()
