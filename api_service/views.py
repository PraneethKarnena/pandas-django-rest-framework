from django.shortcuts import render

from rest_framework import generics


class DatasetListView(generics.ListCreateAPIView):
    pass