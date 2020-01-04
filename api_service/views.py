from django.shortcuts import render

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_service import serializers
from api_service import models


@api_view(['GET', 'POST'])
def datasets_view(request):

    """ List all datasets or create one. """

    data = resp_status = None

    try:
        serializer = None
        if request.method == 'GET':
            # GET request - return all datasets
            datasets = models.DatasetModel.objects.all()
            serializer = serializers.DatasetSerializer(datasets, many=True)
            resp_status = status.HTTP_200_OK

        else:
            # POST request - create a new dataset object
            serializer = serializers.DatasetSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()

                # Store the size of the dataset
                dataset_id = serializer.data.get('id')
                dataset = models.DatasetModel.objects.get(id=dataset_id)
                dataset.size = dataset.file.size
                dataset.save()

                serializer = serializers.DatasetSerializer(dataset, many=False)
                resp_status = status.HTTP_201_CREATED

            else:
                raise Exception(f'{serializer.errors}')

        data = {'success': True, 'data': serializer.data}

    except Exception as e:
        data = {'success': False, 'message': f'Error: {str(e)}'}
        resp_status = status.HTTP_400_BAD_REQUEST

    finally:
        return Response(data=data, status=resp_status)
