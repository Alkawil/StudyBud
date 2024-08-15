from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# models work with database 
class Topic(models.Model): # here topic can have multiple rooms - one to many
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class Room(models.Model):
    host =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
     
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) 


    name = models.CharField(max_length=200)
    descriptions = models.TextField(null=True,blank = True) # null is allowed
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) # takes a snapshot every time we save something
    created = models.DateTimeField(auto_now_add=True) # take a snapshot only once it gets created 


    class Meta:
        ordering = ['-updated','-created']

    def __str__(self): 
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) # one to many relationship - a user can have many messages but all those messages belong to one user

    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # takes a snapshot every time we save something
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]
