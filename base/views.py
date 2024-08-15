from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q #for searching purpose
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

# rooms =  [
#     {'id':1,'name': 'Lets learn python!'},
#     {'id':2,'name': 'Design with me'},
#     {'id':3,'name': 'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:# if the user tries to login using url while being logged in, restrict them
        return redirect('home')
    
    if request.method =="POST": # checking if user has entered the infos and logged in 
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try: # checking if the user already exist
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
              messages.error(request,'Username or password does not exist')



    context={'page':page}

    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() # making sure the username is lowercase
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'base/login_register.html',{'form':form})


def home(request):
    #side and search bar
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(descriptions__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q)) # filter out messages based on browse topic on the left
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}


    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() # calling its children using the name of the class with set.all()/querying child objects
    participants = room.participants.all() #many to many relationship .all()
    if request.method == "POST":
        messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('room',pk=room.id)

    context =  {'room': room,'room_messages': room_messages,'participants':participants}
    return render(request,'base/room.html', context)


def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # since we are using the same name rooms in feed_component.html
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

#create
@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        #request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():

            room = form.save(commit=False) # create an instance of the room
            room.host = request.user
            room.save()
            return redirect('home')


    context = {'form':form}
    return render(request,'base/room_form.html',context)

#update
@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if room.host != request.user:
        return HttpResponse("You are not allowed!!")


    if request.method =="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')

    return render(request,'base/room_form.html',  {'form': form})

#delete
@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if room.host != request.user:
        return HttpResponse("You are not allowed!!")
    
    if request.method =="POST":
        room.delete()
        return redirect('home')

    
    return render(request,'base/delete.html',  {'obj': room})

#delete
@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if message.user != request.user:
        return HttpResponse("You are not allowed!!")
    
    if request.method =="POST":
        message.delete()
        return redirect('home')

    
    return render(request,'base/delete.html',  {'obj': message})


