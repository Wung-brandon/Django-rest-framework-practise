from rest_framework.response import Response
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "desc", "is_complete", "owner"]
        
        def get_owner(self, obj):
            return obj.owner.username