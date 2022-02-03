from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Dataset, Table, Column
from .serializers import GetSingleColumnSerializer, UserSerializer, DatasetSerializer, GetAllDatasetsSerializer, GetSingleDatasetSerializer, TableSerializer, GetAllTablesSerializer, GetSingleTableSerializer, NewTableSerializer, ColumnSerializer, GetAllColumnsSerializer
from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# built in Django user ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
# TableViewSet for table/new url to append a dataset 
# by adding a table without incrementing its version
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('dataset','name','-version','id')
    serializer_class = GetAllTablesSerializer

# APIViews that handle all requests
# dataset view can handle a dataset payload with tables and columns all at once
class DatasetView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, dataset_id=None):
        if dataset_id is not None:
            dataset = Dataset.objects.filter(id = dataset_id).first()
            if dataset is None:
                return Response(
                    {
                        'message': "dataset not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serialized_dataset = GetSingleDatasetSerializer(dataset)
            return Response(serialized_dataset.data)
        datasets = Dataset.objects.all().order_by('name','-version')
        serialized_dataset = GetAllDatasetsSerializer(datasets, many=True, context={'request': request})
        return Response(serialized_dataset.data)
    def post(self, request):
        serialized_dataset = DatasetSerializer(data=request.data)
        if serialized_dataset.is_valid():
            serialized_dataset.save()
            return Response(serialized_dataset.data)
        return Response(serialized_dataset.errors)
    def put(self, request, dataset_id):
        dataset = get_object_or_404(Dataset.objects.all(), id=dataset_id)
        serialized_dataset = DatasetSerializer(instance=dataset, data=request.data, partial=True)
        if serialized_dataset.is_valid(raise_exception=True):
            serialized_dataset.save()
        return Response(serialized_dataset.data, status=204)
    def delete(self, request, dataset_id):
        dataset = get_object_or_404(Dataset.objects.all(), id=dataset_id)
        dataset.delete()
        return Response({"message": "dataset: `{}` has been marked deleted.".format(dataset_id)},status=204)

# table view will first create a new dataset on post requests with an increment view bringing
# all tables along with it and then adding the new table to it based on the request payload
class TableView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, table_id=None):
        if table_id is not None:
            table = Table.objects.filter(id = table_id).first()
            if table is None:
                return Response(
                    {
                        'message': "table not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serialized_table = GetSingleTableSerializer(table)
            return Response(serialized_table.data)
        tables = Table.objects.all().order_by('-dataset','name','-version')
        serialized_table = GetAllTablesSerializer(tables, many=True, context={'request': request})
        return Response(serialized_table.data)
    def post(self, request):
        serialized_table = TableSerializer(data=request.data, many=True)
        if serialized_table.is_valid():
            st = serialized_table.save()
            print('this is my st FLAGG!!!:',st)
            for t in st:
                print(t.id)
                dataset = Dataset.objects.filter(table__id=t.id)
                print(dataset)
                for d in dataset:
                    t.dataset.remove(d)
            for d in dataset:
                all_other_tables = Table.objects.filter(dataset__id = d.id)
                d.pk = None
                d.version = d.version + 1
                d.save()
                for t in st:
                    t.dataset.add(d)
                for t in all_other_tables:
                    t.dataset.add(d)
            return Response(serialized_table.data)
        return Response(serialized_table.errors) 
    def put(self, request, table_id):
        table = get_object_or_404(Table.objects.all(), id=table_id)
        serialized_table = TableSerializer(instance=table, data=request.data, partial=True)
        if serialized_table.is_valid(raise_exception=True):
            serialized_table.save()
        return Response(serialized_table.data, status=204)
    def delete(self, request, table_id):
        table = get_object_or_404(Table.objects.all(), id=table_id)
        table.delete()
        return Response({"message": "table: `{}` has been marked deleted.".format(table_id)},status=204)

# basic APIView to handle any column requests
class ColumnView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, column_id=None):
        if column_id is not None:
            column = Column.objects.filter(id = column_id).first()
            if column is None:
                return Response(
                    {
                        'message': 'column not found, make sure you have the correct id'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serialized_column = GetSingleColumnSerializer(column)
            return Response(serialized_column.data)
        all_columns = Column.objects.all().order_by('table','name')
        serialized_columns = GetAllColumnsSerializer(all_columns, many=True, context={'request': request})
        return Response(serialized_columns.data)
    def post(self,request):
        serialized_column = GetAllColumnsSerializer(data=request.data, many=True)
        if serialized_column.is_valid():
            serialized_column.save()
        return Response(serialized_column.data)
    def put(self,request,column_id):
        column = get_object_or_404(Column.objects.all(), id=column_id)
        serialized_column = ColumnSerializer(instance=column, data=request.data, partial=True)
        if serialized_column.is_valid(raise_exception=True):
            serialized_column.save()
        return Response(serialized_column.data, status=204)
    def delete(self,request,column_id):
        column = get_object_or_404(Column.objects.all(), id=column_id)
        column.delete()
        return Response({'message':'column: `{}` has been deleted'.format(column_id)}, status=204)

# TRUNCATE VIEWS
# will create a new dataset with no tables and increments its version
# will then add new tables based on the request payload passed in 
class DatasetTruncateView(APIView):
    def get(self, request, dataset_id=None):
        dataset = Dataset.objects.filter(id = dataset_id).first()
        if dataset is None:
            return Response(
                {
                    'message': "dataset not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serialized_dataset = DatasetSerializer(dataset)
        return Response(serialized_dataset.data)
    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset.objects.filter(id = dataset_id))
        # dataset.deleted = True
        # dataset.save()
        dataset.pk = None
        dataset.version = dataset.version + 1
        dataset.save()
        serialized_tables = NewTableSerializer(data=request.data, many=True)
        if serialized_tables.is_valid():
            st = serialized_tables.save()
        for table in st:
            table.dataset.add(dataset)
        return Response({"message": "dataset: `{}` has been truncated.".format(dataset_id)},status=204)

# will create a new dataset with no tables and increments its version
# will create a new table with no columns and increments its version and assign it to the new dataset from above
# will then add the new columns based on the request payload passed in 
class TableTruncateView(APIView):
    def get(self, request, table_id=None):
        table = Table.objects.filter(id = table_id).first()
        if table is None:
            return Response(
                {
                    'message': "table not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serialized_table = GetSingleTableSerializer(table)
        return Response(serialized_table.data)
    def post(self, request, table_id):
        dataset = Dataset.objects.filter(table__id = table_id).last()
        table = get_object_or_404(Table.objects.filter(id = table_id))
        tables = Table.objects.filter(dataset__id = dataset.id)
        dataset.pk = None
        dataset.version = dataset.version + 1
        dataset.save()
        for t in tables:
            t.dataset.add(dataset)
        table.dataset.remove(dataset)
        # table.deleted = True
        # table.save()
        table.pk = None
        table.version = table.version + 1
        table.save()
        table.dataset.add(dataset)
        serialized_columns = GetAllColumnsSerializer(data=request.data, many=True)
        if serialized_columns.is_valid():
            sc = serialized_columns.save()
            print(sc)
            for column in sc:
                column.table = table
                column.save()
        return Response({"message": "table: `{}` has been truncated.".format(table_id)},status=204)
