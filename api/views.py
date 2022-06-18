import imp
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Board
from .serializers import BoardSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import BoardDetailSerializer
from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main.models import Comment
from .serializers import CommentSerializer

@api_view(['GET'])
def boards(request):
    if request.method == 'GET':
        boards = Board.objects.filter(is_active=True)[:10]
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

class BoardDetailView(RetrieveAPIView):
    queryset = Board.objects.filter(is_active=True)
    serializer_class = BoardDetailSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,)) # класс разграничения доступа
def comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, board=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)