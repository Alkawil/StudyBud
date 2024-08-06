from django.shortcuts import render,redirect
from django.db.models import Q #for searching purpose
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.

# rooms =  [
#     {'id':1,'name': 'Lets learn python!'},
#     {'id':2,'name': 'Design with me'},
#     {'id':3,'name': 'Frontend developers'},
# ]
def home(request):
    #side and search bar
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(descriptions__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()

    return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_count':room_count})

def room(request,pk):
    room = Room.objects.get(id=pk)
    return render(request,'base/room.html',  {'room': room})

#create
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        #request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request,'base/room_form.html',context)

#update
def update_room(request,pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)
    if request.method =="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')

    return render(request,'base/room_form.html',  {'form': form})

def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method =="POST":
        room.delete()
        return redirect('home')

    
    return render(request,'base/delete.html',  {'obj': room})


