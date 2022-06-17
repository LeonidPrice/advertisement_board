import imp
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Board
from .serializer import BoardSerializer
from rest_framework.generics import RetrieveAPIView
from .serializer import BoardDetailSerializer

@api_view(['GET'])
def boards(request):
    if request.method == 'GET':
        boards = Board.objects.filter(is_active=True)[:10]
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

class BoardDetailView(RetrieveAPIView):
    queryset = Board.objects.filter(is_active=True)
    serializer_class = BoardDetailSerializer