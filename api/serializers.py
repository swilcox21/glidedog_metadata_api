from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Dataset, Table, Column

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

# serializers for creating tables with nested columns in payload
class AnotherTableSerializer(serializers.ModelSerializer):  # needed another table serializer in order to create tables
    class Meta:                                             # with the columns included in the payload
        model = Table
        fields = '__all__'        
class ColumnSerializer(serializers.ModelSerializer):
    table = AnotherTableSerializer(required=False)
    class Meta:
        model = Column
        fields = '__all__'
class TableSerializer(serializers.ModelSerializer):
    column = ColumnSerializer(many=True, required=False)
    class Meta:
        model = Table
        fields = '__all__'
    def create(self, validated_data):
        all_columns_data = validated_data.pop('column')
        table = super(TableSerializer, self).create(validated_data)
        if all_columns_data is not None:
            for column_data in all_columns_data:
                Column.objects.create(table=table, **column_data)
        return table

# serializers for gets only 
#   (full lists 'All' exclude children to read easier)
class GetAllDatasetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'
class GetAllTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
class GetAllColumnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'
#   (single gets that include children)
class GetSingleColumnSerializer(serializers.ModelSerializer):
    table = AnotherTableSerializer(required=False, read_only=True)
    class Meta:
        model = Column
        fields = ['id','name','type','rows','table']
class GetSingleTableSerializer(serializers.ModelSerializer):
    column = GetAllColumnsSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Table
        fields = ['id','name','rows','version','current','dataset','column']  
class GetSingleDatasetSerializer(serializers.ModelSerializer):
    table = GetSingleTableSerializer(required=False, read_only=True, many=True)
    class Meta:
        model = Dataset
        fields = ['id','name','owner','version','current','table']

# serializers for INITIAL DATASET COMMIT below 
# (can handle full payload for one dataset with tables and columns included)
class NewColumnSerializer(serializers.ModelSerializer):
    table = TableSerializer(required=False)
    class Meta:
        model = Column
        fields = '__all__'
class NewTableSerializer(serializers.ModelSerializer):
    column = NewColumnSerializer(many=True, required=False)
    class Meta:
        model = Table
        exclude = ('dataset',)
    def create(self, validated_data):
        all_columns_data = validated_data.pop('column')
        table = super(NewTableSerializer, self).create(validated_data)
        if all_columns_data is not None:
            for column_data in all_columns_data:
                Column.objects.create(table=table, **column_data)
        return table
class DatasetSerializer(serializers.ModelSerializer):
    table = NewTableSerializer(many=True, required=False)
    class Meta:
        model = Dataset
        fields = '__all__'
        # VALIDATE FOR TROUBLESHOOTING
    def validate(self, data):
            cloned_data = data.copy()
            del cloned_data['table']
            super(DatasetSerializer, self).validate(cloned_data)
            return data
    def create(self, validated_data):
        all_tables_data = validated_data.pop('table')
        dataset = super(DatasetSerializer, self).create(validated_data)
        if all_tables_data is not None:
            for table_data in all_tables_data:
                table_s = NewTableSerializer(data=table_data)
                if table_s.is_valid():
                    t = table_s.save()
                    dataset.table.add(t)
        return dataset

