from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'login_reg/index.html')

def register(request):

    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.create_user(request.POST)
        request.session['user_id'] = new_user.id
    return redirect('/travels')

def travels(request):
    if not 'user_id' in request.session.keys():
        print "no user here"
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "user_travel": Trip.objects.filter(creator_id = request.session['user_id']),
        "user_not_travel": Trip.objects.exclude(followers__id = request.session['user_id']).exclude(creator_id=request.session['user_id']),
        "followed_travel": Trip.objects.filter(followers__id = request.session['user_id']).exclude(creator_id=request.session['user_id'])
    }
    return render(request, 'login_reg/travels.html', context)

def login(request):
    result = User.objects.validate_login(request.POST)
    if result[0]:
        for e in result[0]:
            messages.error(request, e)
            return redirect('/')
    else:
        request.session['user_id'] = result[1].id
        return redirect('/travels')

def logout(request):
    for sesh in request.session.keys():
        del request.session[sesh]
    return redirect('/')

def add(request):
    return render(request, 'login_reg/add_trip.html')

def post_add(request):
    errors = Trip.objects.validate_trip(request.POST)
    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('/add')
    else:
        Trip.objects.create_trip(request.POST, request.session['user_id'])
    return redirect('/travels')

def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    trip.followers.add(user)
    return redirect('/travels')

def destination(request, trip_id):
    context = {
        "trip": Trip.objects.get(id=trip_id),
        "followed_travel": User.objects.filter(follows=trip_id),
    }
    return render(request, 'login_reg/display_trip.html', context)
