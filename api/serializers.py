from dataclasses import fields
from rest_framework import serializers
from main.models import Board
from main.models import Comment

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('board', 'author', 'content', 'created_at')
