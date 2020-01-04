from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_service import serializers
from api_service import models
from api_service import tasks


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

                # Begin processing using Pandas
                tasks.process_dataset.delay(dataset_id)

            else:
                raise Exception(f'{serializer.errors}')

        data = {'success': True, 'data': serializer.data}

    except Exception as e:
        data = {'success': False, 'message': f'Error: {str(e)}'}
        resp_status = status.HTTP_400_BAD_REQUEST

    finally:
        return Response(data=data, status=resp_status)


class DatasetDetailView(generics.RetrieveUpdateDestroyAPIView):

    """ Read/Update/Delete a single dataset """

    queryset = models.DatasetModel.objects.all()
    serializer_class = serializers.DatasetSerializer


@api_view(['GET'])
def export_data(request, pk, export_type):
    try:
        export_type = export_type.lower()
        if export_type not in ('excel', 'stats', 'plot'):
            raise Exception('Bad format requested.')

        dataset = models.DatasetModel.objects.get(pk=pk)
        data = {'success': True, 'data': 'Still being processed.'}
        resp_status = status.HTTP_200_OK

        if export_type == 'excel' and dataset.excel_creation_status == 'CRT':
            data = {'success': True, 'data': f'{dataset.excel_url}'}

        if export_type == 'stats' and dataset.stats_creation_status == 'CRT':
            data = {'success': True, 'data': f'{dataset.stats}'}

        if export_type == 'plot' and dataset.pdf_creation_status == 'CRT':
            data = {'success': True, 'data': f'{dataset.pdf_url}'}

    except Exception as e:
        data = {'success': False, 'message': f'Error: {str(e)}'}
        resp_status = status.HTTP_400_BAD_REQUEST

    finally:
        return Response(data=data, status=resp_status)