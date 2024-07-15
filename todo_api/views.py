from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from django_filters import rest_framework as filters

# Create your views here.
class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, )
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
    
class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

# class CreateTodoAPIView(CreateAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (IsAuthenticated, )
    
#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)

# class ListTodoAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (IsAuthenticated,)
#     queryset = Todo.objects.all() # get all the todos created from the database 
    
#     def get_queryset(self):
#         return Todo.objects.filter(owner=self.request.user) # returns all the todos created by the authenticated user