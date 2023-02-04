from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
from django.core.files.storage import FileSystemStorage
import uuid
from django.http.multipartparser import MultiPartParser
import json

def index(request):
    context = {}

    return render(request, 'main.html', context)