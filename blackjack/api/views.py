import pdb
import json

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404



@api_view(["GET"])
def deal(request):
    return JsonResponse(status=status.HTTP_200_OK)