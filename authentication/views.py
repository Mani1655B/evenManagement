# Import necessary modules and models
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from .models import *

# Define a view function for the home page
def home(request):
	events=Event.objects.all()
	user=request.user
	if  not user.is_authenticated:
		return render(request, 'authentication/index.html',{'images':Photos.objects.all(),'events':events})

	role=Profile.objects.get(user=user).role
	print(role)
	return render(request, 'authentication/index.html',{'images':Photos.objects.all(),'events':events,'role':role})

# Define a view function for the login page
def login_page(request):
	# Check if the HTTP request method is POST (form submission)
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		# Check if a user with the provided username exists
		if not User.objects.filter(username=username).exists():
			# Display an error message if the username does not exist
			messages.error(request, 'Invalid Username')
			return redirect('/login/')
		
		# Authenticate the user with the provided username and password
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			# recipiant=[user.email,]
			# send_mail( 'login', 'some one is is loged in into user account', from_email=settings.EMAIL_HOST_USER, recipient_list=recipiant )

		
		if user is None:
			# Display an error message if authentication fails (invalid password)
			messages.error(request, "Invalid Password")
			return redirect('/login/')
		else:
			# Log in the user and redirect to the home page upon successful login
			login(request, user)
			return redirect('/')
	
	# Render the login page template (GET request)
	return render(request, 'authentication/login.html')

# Define a view function for the registration page
def signin_page(request):
	# Check if the HTTP request method is POST (form submission)
	if request.method == 'POST':
		first_name = request.POST.get('firstname')
		last_name = request.POST.get('lastname')
		username = request.POST.get('username')
		email=request.POST.get('email')
		password = request.POST.get('password')
		
		# Check if a user with the provided username already exists
		user = User.objects.filter(username=username)
		
		if user.exists():
			# Display an information message if the username is taken
			messages.info(request, "Username already taken!")
			return redirect('/signup/')
		
		# Create a new User object with the provided information
		user = User.objects.create_user(
			first_name=first_name,
			last_name=last_name,
			username=username,
			email=email
		)
		
		# Set the user's password and save the user object
		user.set_password(password)
		user.save()
		
		# Display an information message indicating successful account creation
		messages.info(request, "Account created Successfully!")
		return redirect('/login/')
	
	# Render the registration page template (GET request)
	return render(request, 'authentication/signup.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def contact(request):
	if request.method=="GET":
		name=request.GET.get('name')
		mail=request.GET.get('mail')
		number=request.GET.get('number')
		subject=request.GET.get('subject')
		message=request.GET.get('message')
		temp=Contact(name=name,mail=mail,number=number,subject=subject,message=message)
		temp.save()
		return redirect('/')
	
def register(request):
	if request.method=="POST":
		event_name=request.POST.get('event_name')
		print(event_name)
		user=request.user
		r1=Registration(event=Event.objects.get(name=event_name),user=Profile.objects.get(user=user))
		r1.save()
		return redirect('/')
	

def recruit(request):
	if request.method=="POST":
		pass
	return render(request,"authentication/register.html")

def myevents(request):
	try:
		user = request.user
		registrations = Registration.objects.filter(user=Profile.objects.get(user=user))
		events = [registration.event for registration in registrations]
		return render(request, 'authentication/myevents.html', {'events': events})
	except:
		return redirect('/login/')
	

def pastevents(request):
	events=Event.objects.filter(end_time__lt=datetime.date.today)
	return render(request, 'authentication/pastevents.html',{'images':Photos.objects.all(),'events':events})


def organizerevents(request):
	return render(request,'authentication/org.html')







