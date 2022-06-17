from dataclasses import fields
from rest_framework import serializers
from main.models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 
            'title', 
            'content', 
            'price', 
            'created_at')

class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id',
            'title',
            'content',
            'price',
            'created_at',
            'contacts',
            'image')