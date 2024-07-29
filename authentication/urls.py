from django.urls import path


from .views import login_page,signin_page,home,logout,contact,register,recruit,myevents,organizerevents
urlpatterns = [
    path('',home,name='home'),
    path('login/',login_page,name='login'),
    path('signup/',signin_page,name='signup'),
    path('logout/',logout,name='logout'),
    path('contact/',contact,name='contact'),
    path('register/',register,name='register'),
    path('recruit/',recruit,name='recrute'),
    path('myevents/',myevents,name='myevents'),
    path('organizer_events/',organizerevents,name='organizerevents'),
]


